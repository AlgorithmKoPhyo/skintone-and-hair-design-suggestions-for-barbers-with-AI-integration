"""
==========================================================================
StyleMe AI - Hairstyle DAO Layer (Data Access Object)
==========================================================================
This module handles raw data access and returns Python dummy dataset records.
Can be easily upgraded to ORM/SQLAlchemy/MySQL without affecting Service Layer.
"""

class HairstyleDAO:
    def __init__(self):
        self._analysis_logs = []
        
        import firebase_admin
        from firebase_admin import credentials
        from firebase_admin import firestore
        
        # Initialize firebase admin if not already initialized
        if not firebase_admin._apps:
            try:
                import os
                # Look for a service account key file in the root directory
                cred_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'firebase-credentials.json')
                
                if os.path.exists(cred_path):
                    cred = credentials.Certificate(cred_path)
                    firebase_admin.initialize_app(cred)
                    print("Firebase Admin initialized with service account key.")
                else:
                    # Fallback to Application Default Credentials
                    firebase_admin.initialize_app()
                    print("Firebase Admin initialized with default credentials.")
            except Exception as e:
                print("Failed to initialize firebase_admin:", e)
        
        try:
            self.db = firestore.client()
        except Exception as e:
            self.db = None
            print("Failed to initialize firestore client:", e)
            
        # In-memory cache for simplicity and performance, can be improved with TTL
        self._cache = None
        self._cache_time = 0

    def _fetch_all_from_firebase(self, force_refresh=False):
        import time
        
        # Cache for 1 hour (3600 seconds) to prevent slow page loads
        if not force_refresh and self._cache is not None and (time.time() - self._cache_time) < 3600:
            return self._cache
            
        try:
            if not self.db:
                print("Firestore client is not initialized.")
                return []
                
            hairstyles_ref = self.db.collection('hairstyles')
            docs = hairstyles_ref.stream()
            
            parsed_docs = []
            for doc in docs:
                d = doc.to_dict()
                d['id'] = doc.id
                # The frontend JS and other logic might expect 'slug' to be correctly set,
                # which it should be if it's stored in Firestore properly.
                parsed_docs.append(d)
                
            self._cache = parsed_docs
            self._cache_time = time.time()
                
            return self._cache or []
            
        except Exception as e:
            print(f"Exception fetching from Firestore admin: {e}")
            return self._cache or []

    def get_all_hairstyles(self, gender=None, shape=None, search=None, category=None):
        results = self._fetch_all_from_firebase()

        if gender and gender != 'all':
            results = [item for item in results if item.get("gender") == gender]

        if shape and shape != 'all':
            results = [item for item in results if item.get("faceshape") == shape or item.get("ideal_shape") == shape]
            
        if category and category != 'all':
            # Case insensitive comparison for category
            cat_lower = category.lower()
            results = [item for item in results if item.get("category") and item.get("category").lower() == cat_lower]

        if search:
            search_str = search.lower()
            results = [item for item in results if search_str in item.get("name", "").lower()]

        return results

    def get_hairstyle_by_slug(self, slug):
        results = self._fetch_all_from_firebase()
        for item in results:
            if item.get("slug") == slug:
                return item
        return None

    def get_recommendation_by_shape_and_gender(self, gender, shape):
        results = self._fetch_all_from_firebase()
        
        # 1. Exact match by gender & faceshape
        for item in results:
            if item.get("gender") == gender and (item.get("faceshape") == shape or item.get("ideal_shape") == shape):
                return item

        # 2. Fallback to gender match
        for item in results:
            if item.get("gender") == gender:
                return item

        # 3. Default first item
        return results[0] if results else None

    def get_related_hairstyles(self, gender=None, shape=None, current_slug=None, limit=5):
        results = self._fetch_all_from_firebase()
        
        seen_categories = set()
        
        # Optionally exclude the category of the current_slug itself
        if current_slug:
            for item in results:
                if item.get("slug") == current_slug:
                    cat = item.get("category")
                    if cat:
                        seen_categories.add(cat.lower())
                    break

        # 1. Primary matching by gender and faceshape (excluding current_slug)
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

        # 2. Backfill with same gender if needed (maintaining unique categories)
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
        log_entry = {
            "id": len(self._analysis_logs) + 1,
            "user_image_url": user_image_url,
            "detected_shape": detected_shape,
            "gender": gender,
            "analysis_type": analysis_type,
            "confidence": confidence
        }
        self._analysis_logs.append(log_entry)
        return log_entry

