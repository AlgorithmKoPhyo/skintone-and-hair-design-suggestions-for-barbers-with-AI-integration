"""
==========================================================================
StyleMe AI - Hairstyle Service Layer (Business Logic)
==========================================================================
Encapsulates business rules and communicates with the DAO layer.
Follows Request -> Service -> DAO clean architecture.
"""

from app.dao.hairstyle_dao import HairstyleDAO

class HairstyleService:
    def __init__(self):
        self.dao = HairstyleDAO()

    def get_all_hairstyles(self, gender=None, shape=None, search=None):
        """Retrieve all catalog hairstyles with optional filtering."""
        return self.dao.get_all_hairstyles(gender=gender, shape=shape, search=search)

    def get_hairstyle_by_slug(self, slug):
        """Retrieve single hairstyle details by slug key."""
        if not slug:
            return None
        return self.dao.get_hairstyle_by_slug(slug)

    def get_recommendation(self, gender='female', shape='oval'):
        """Get best AI recommendation matching user gender and face shape."""
        gender = gender if gender in ['female', 'male'] else 'female'
        shape = shape if shape in ['oval', 'round', 'square', 'heart'] else 'oval'
        return self.dao.get_recommendation_by_shape_and_gender(gender, shape)

    def get_related_hairstyles(self, gender='female', shape='oval', current_slug=None, limit=6):
        """Get related hairstyles matching gender and face shape."""
        return self.dao.get_related_hairstyles(gender=gender, shape=shape, current_slug=current_slug, limit=limit)

    def log_user_analysis(self, user_image_url, detected_shape, gender, analysis_type='hairstyle', confidence=0.96):
        """Log user photo analysis session via DAO layer."""
        return self.dao.save_analysis_log(
            user_image_url=user_image_url,
            detected_shape=detected_shape,
            gender=gender,
            analysis_type=analysis_type,
            confidence=confidence
        )
