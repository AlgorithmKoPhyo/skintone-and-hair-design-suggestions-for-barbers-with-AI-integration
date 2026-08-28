import os
import sqlite3
import json
import requests
import uuid
from urllib.parse import urlparse

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'app', 'firebase_offline.db')
IMAGE_DIR = os.path.join(BASE_DIR, 'app', 'static', 'images', 'firebase_data')
CRED_PATH = os.path.join(BASE_DIR, 'firebase-credentials.json')

# Ensure directories exist
os.makedirs(IMAGE_DIR, exist_ok=True)

import hashlib

def download_image(url):
    """Downloads an image from a URL and returns the local static path."""
    if not url or not url.startswith('http'):
        return url # Already a local path or empty

    try:
        # Clean up extension if it has weird query params
        parsed_url = urlparse(url)
        path = parsed_url.path
        ext = os.path.splitext(path)[1]
        if not ext:
            ext = '.jpg' # Fallback extension
        ext = ext.split('?')[0]

        # Use MD5 hash of URL to avoid duplicate downloads
        url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()
        filename = f"{url_hash}{ext}"
        local_filepath = os.path.join(IMAGE_DIR, filename)
        web_path = f"/static/images/firebase_data/{filename}"

        if os.path.exists(local_filepath):
            return web_path

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        with open(local_filepath, 'wb') as f:
            f.write(response.content)

        return web_path
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return url

def setup_sqlite():
    """Initializes the SQLite database with the required schema."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Drop existing table to remove UNIQUE constraint
    cursor.execute('DROP TABLE IF EXISTS hairstyles')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hairstyles (
            id TEXT PRIMARY KEY,
            slug TEXT NOT NULL,
            gender TEXT,
            faceshape TEXT,
            category TEXT,
            name TEXT,
            full_data_json TEXT NOT NULL
        )
    ''')
    
    # We can also add user_analyses if needed, but the original code had it in styleme.db
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_image_url TEXT NOT NULL,
            detected_shape TEXT NOT NULL,
            gender TEXT NOT NULL,
            analysis_type TEXT DEFAULT 'hairstyle',
            confidence REAL DEFAULT 0.96,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    return conn

def main():
    print("Starting Firebase to SQLite Migration...")
    
    # Initialize Firebase
    if not os.path.exists(CRED_PATH):
        print(f"Error: Firebase credentials not found at {CRED_PATH}")
        return

    cred = credentials.Certificate(CRED_PATH)
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    print("Connected to Firebase Firestore.")
    
    conn = setup_sqlite()
    cursor = conn.cursor()

    print("SQLite Database created/connected.")

    # Fetch all hairstyles into memory first to avoid Firestore stream timeouts
    print("Fetching all hairstyles from Firestore...")
    hairstyles_ref = db.collection('hairstyles')
    docs = hairstyles_ref.stream()
    
    all_hairstyles = []
    for doc in docs:
        data = doc.to_dict()
        data['_id'] = doc.id
        all_hairstyles.append(data)
        
    print(f"Fetched {len(all_hairstyles)} hairstyles. Beginning parallel downloads...")

    import concurrent.futures

    def process_hairstyle(data):
        doc_id = data.pop('_id')
        slug = data.get('slug', doc_id)
        
        # 1. Download main image
        if 'main_img' in data and data['main_img']:
            data['main_img'] = download_image(data['main_img'])
            
        # 2. Download angles images
        if 'angles' in data and isinstance(data['angles'], list):
            for i, angle in enumerate(data['angles']):
                if isinstance(angle, dict) and 'img' in angle:
                    data['angles'][i]['img'] = download_image(angle['img'])
                    
        # Extract fields for easy querying
        gender = data.get('gender')
        faceshape = data.get('faceshape', data.get('ideal_shape'))
        category = data.get('category')
        name = data.get('name')
        
        # Serialize the updated dict to JSON
        full_data_json = json.dumps(data)
        
        return (doc_id, slug, gender, faceshape, category, name, full_data_json)

    total_migrated = 0
    results = []
    
    # Run downloads in parallel using 15 workers
    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        # submit tasks and show progress
        future_to_data = {executor.submit(process_hairstyle, data): data for data in all_hairstyles}
        for future in concurrent.futures.as_completed(future_to_data):
            try:
                res = future.result()
                results.append(res)
                print(f"Processed: {res[5] or res[1]} ({len(results)}/{len(all_hairstyles)})")
            except Exception as exc:
                print(f"Hairstyle processing generated an exception: {exc}")

    print("\nSaving to SQLite database...")
    for res in results:
        # Insert or Replace into SQLite
        cursor.execute('''
            INSERT OR REPLACE INTO hairstyles 
            (id, slug, gender, faceshape, category, name, full_data_json)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', res)
        total_migrated += 1

    conn.commit()
    conn.close()

    print(f"\nParallel Migration Complete! Total items migrated: {total_migrated}")
    print(f"Database saved to: {DB_PATH}")
    print(f"Images saved to: {IMAGE_DIR}")

if __name__ == '__main__':
    main()
