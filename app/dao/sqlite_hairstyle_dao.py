"""
==========================================================================
StyleMe AI - Hairstyle DAO Layer (SQLite Version)
==========================================================================
This module replaces the Firebase DAO. It reads data and images directly 
from a local SQLite database (firebase_offline.db), ensuring 100% offline capability.
"""

import sqlite3
import json
import os
import random

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'firebase_offline.db')

class SqliteHairstyleDAO:
    def __init__(self):
        self._analysis_logs = []
        
        # Ensure database exists, if not, print a warning.
        if not os.path.exists(DB_PATH):
            print(f"⚠️ Warning: Database not found at {DB_PATH}. Please run the migration script.")

    def _get_db(self):
        """Creates and returns a new database connection."""
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    def _format_row(self, row):
        """Parses the JSON string back into a Python dictionary."""
        if not row or 'full_data_json' not in row.keys():
            return None
        
        try:
            data = json.loads(row['full_data_json'])
            # Ensure the ID is attached if it wasn't in the JSON
            if 'id' not in data and 'id' in row.keys():
                data['id'] = row['id']
            return data
        except Exception as e:
            print(f"Error parsing JSON from SQLite: {e}")
            return None

    def _fetch_all(self):
        """Helper to fetch all records (used mostly for complex filtering)."""
        if not os.path.exists(DB_PATH):
            return []
            
        conn = self._get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM hairstyles")
        rows = cursor.fetchall()
        conn.close()
        
        return [self._format_row(row) for row in rows if row]

    def get_all_hairstyles(self, gender=None, shape=None, search=None, category=None):
        if not os.path.exists(DB_PATH):
            return []
            
        conn = self._get_db()
        cursor = conn.cursor()
        
        query = "SELECT * FROM hairstyles WHERE 1=1"
        params = []

        if gender and gender != 'all':
            query += " AND gender = ?"
            params.append(gender)

        if shape and shape != 'all':
            query += " AND faceshape = ?"
            params.append(shape)
            
        if category and category != 'all':
            query += " AND LOWER(category) = ?"
            params.append(category.lower())

        if search:
            query += " AND LOWER(name) LIKE ?"
            params.append(f"%{search.lower()}%")

        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        return [self._format_row(row) for row in rows if row]

    def get_hairstyle_by_slug(self, slug):
        if not os.path.exists(DB_PATH):
            return None
            
        conn = self._get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM hairstyles WHERE slug = ?", (slug,))
        row = cursor.fetchone()
        conn.close()
        
        return self._format_row(row)

    def get_recommendation_by_shape_and_gender(self, gender, shape):
        if not os.path.exists(DB_PATH):
            return None
            
        conn = self._get_db()
        cursor = conn.cursor()
        
        # 1. Exact match by gender & faceshape
        cursor.execute("SELECT * FROM hairstyles WHERE gender = ? AND faceshape = ?", (gender, shape))
        exact_matches = cursor.fetchall()
        
        if exact_matches:
            conn.close()
            return self._format_row(random.choice(exact_matches))

        # 2. Fallback to gender match
        cursor.execute("SELECT * FROM hairstyles WHERE gender = ?", (gender,))
        gender_matches = cursor.fetchall()
        
        conn.close()
        
        if gender_matches:
            return self._format_row(random.choice(gender_matches))

        # 3. Default random item
        all_results = self._fetch_all()
        return random.choice(all_results) if all_results else None

    def get_related_hairstyles(self, gender=None, shape=None, current_slug=None, limit=5):
        results = self._fetch_all()
        random.shuffle(results)
        
        seen_categories = set()
        
        if current_slug:
            for item in results:
                if item.get("slug") == current_slug:
                    cat = item.get("category")
                    if cat:
                        seen_categories.add(cat.lower())
                    break

        # 1. Primary matching by gender and faceshape
        primary_matches = []
        for item in results:
            if current_slug and item.get("slug") == current_slug:
                continue
            if gender and gender != 'all' and item.get("gender") != gender:
                continue
                
            cat = item.get("category")
            cat_lower = cat.lower() if cat else "uncategorized"
            
            if cat_lower in seen_categories:
                continue

            if shape and shape != 'all' and (item.get("faceshape") == shape or item.get("ideal_shape") == shape):
                primary_matches.append(item)
                seen_categories.add(cat_lower)
                
            if len(primary_matches) >= limit:
                break

        if len(primary_matches) >= limit:
            return primary_matches

        # 2. Backfill with same gender if needed
        fetched_slugs = {item.get("slug") for item in primary_matches}
        if current_slug:
            fetched_slugs.add(current_slug)

        backfill_matches = []
        for item in results:
            if item.get("slug") in fetched_slugs:
                continue
            if gender and gender != 'all' and item.get("gender") != gender:
                continue
                
            cat = item.get("category")
            cat_lower = cat.lower() if cat else "uncategorized"
            
            if cat_lower in seen_categories:
                continue

            backfill_matches.append(item)
            seen_categories.add(cat_lower)
            
            if len(primary_matches) + len(backfill_matches) >= limit:
                break

        return primary_matches + backfill_matches

    def save_analysis_log(self, user_image_url, detected_shape, gender, analysis_type='hairstyle', confidence=0.96):
        if not os.path.exists(DB_PATH):
            print("Warning: Cannot save analysis log, database does not exist.")
            return None
            
        conn = self._get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO user_analyses (user_image_url, detected_shape, gender, analysis_type, confidence)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_image_url, detected_shape, gender, analysis_type, confidence))
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        
        log_entry = {
            "id": last_id,
            "user_image_url": user_image_url,
            "detected_shape": detected_shape,
            "gender": gender,
            "analysis_type": analysis_type,
            "confidence": confidence
        }
        self._analysis_logs.append(log_entry)
        return log_entry
