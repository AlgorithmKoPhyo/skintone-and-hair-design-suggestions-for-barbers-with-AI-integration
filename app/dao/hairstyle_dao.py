"""
==========================================================================
StyleMe AI - Hairstyle DAO Layer (Data Access Object)
==========================================================================
This module handles raw data access and returns Python dummy dataset records.
Can be easily upgraded to ORM/SQLAlchemy/MySQL without affecting Service Layer.
"""

class HairstyleDAO:
    def __init__(self):
        # In-Memory Dummy Hairstyles Dataset (Female & Male across Oval, Round, Square, Heart)
        self._hairstyles = [
            # --- FEMALE HAIRSTYLES ---
            {
                "id": 1,
                "slug": "classic_bob",
                "name": "Classic Bob Cut",
                "tagline": "Timeless chin-length cut enhancing natural symmetry.",
                "gender": "female",
                "faceshape": "oval",
                "ideal_shape": "oval",
                "shape_badge": "Ideal for Oval Face",
                "score_badge": "95% Match",
                "main_img": "/static/images/classic_bob.jpg",
                "description": "Chin-length classic haircut with clean ends that frames oval faces with timeless symmetry and sophisticated balance.",
                "hair_length": "Chin Length",
                "hair_texture": "Straight / Soft Waves",
                "styling_time": "10 - 15 mins",
                "maintenance": "Easy",
                "reasons": [
                    "Maintains the natural balance of your face shape",
                    "Frames your face beautifully with chin-length curves",
                    "Adds a youthful, elegant, and fresh aesthetic",
                    "Easy to style and low maintenance"
                ],
                "suitability": [
                    {"shape": "Oval Face", "score": "95% (Ideal)"},
                    {"shape": "Heart Face", "score": "92% (Great)"},
                    {"shape": "Round Face", "score": "85% (Good)"},
                    {"shape": "Square Face", "score": "80% (Moderate)"}
                ],
                "tips": [
                    "Blow dry with a round brush for inward natural end curves.",
                    "Tuck one side behind the ear for an effortless chic look.",
                    "Use heat protectant spray before using flat irons.",
                    "A lightweight finishing oil keeps ends glossy and smooth."
                ],
                "angles": [
                    {"name": "Front", "img": "/static/images/classic_bob.jpg"},
                    {"name": "Side", "img": "/static/images/bob_cut_side.jpg"},
                    {"name": "3/4 View", "img": "/static/images/bob_cut_34.jpg"},
                    {"name": "Back", "img": "/static/images/bob_cut_back.jpg"}
                ]
            },
            {
                "id": 2,
                "slug": "curtain_bangs_waves",
                "name": "Curtain Bangs & Long Waves",
                "tagline": "Soft cheekbone framing curtain bangs with flowing waves.",
                "gender": "female",
                "faceshape": "oval",
                "ideal_shape": "oval",
                "shape_badge": "Ideal for Oval Face",
                "score_badge": "96% Match",
                "main_img": "/static/images/hero_model.jpg",
                "description": "Soft sweeping curtain bangs paired with long cascading waves that accentuate cheekbones and natural facial balance.",
                "hair_length": "Long / Mid-Back",
                "hair_texture": "Soft Waves",
                "styling_time": "15 - 20 mins",
                "maintenance": "Moderate",
                "reasons": [
                    "Curtain bangs sweep outward to highlight cheekbones",
                    "Long soft waves elongate silhouette gracefully",
                    "Highlights symmetrical oval facial proportions",
                    "Versatile styling options for formal or casual looks"
                ],
                "suitability": [
                    {"shape": "Oval Face", "score": "96% (Ideal)"},
                    {"shape": "Round Face", "score": "91% (Great)"},
                    {"shape": "Heart Face", "score": "89% (Great)"}
                ],
                "tips": [
                    "Blow dry curtain bangs away from the face with a medium barrel brush.",
                    "Use a large curling wand for loose flowing waves."
                ],
                "angles": [
                    {"name": "Front", "img": "/static/images/hero_model.jpg"},
                    {"name": "Side", "img": "/static/images/hero_model.jpg"},
                    {"name": "3/4 View", "img": "/static/images/hero_model.jpg"},
                    {"name": "Back", "img": "/static/images/hero_model.jpg"}
                ]
            },
            {
                "id": 3,
                "slug": "textured_bob",
                "name": "Textured Long Bob (Lob)",
                "tagline": "Collarbone length with subtle layers elongating face shape.",
                "gender": "female",
                "faceshape": "round",
                "ideal_shape": "round",
                "shape_badge": "Ideal for Round Face",
                "score_badge": "92% Match",
                "main_img": "/static/images/textured_bob.jpg",
                "description": "Collarbone length with subtle layers that elongate round faces and soften cheek curves with light vertical body.",
                "hair_length": "Collarbone",
                "hair_texture": "Textured / Wavy",
                "styling_time": "15 mins",
                "maintenance": "Moderate",
                "reasons": [
                    "Creates subtle vertical lines to elongate facial proportions",
                    "Softens jawline curves with textured waves",
                    "Adds height and body at the crown",
                    "Flatters cheekbones without adding side bulk"
                ],
                "suitability": [
                    {"shape": "Round Face", "score": "92% (Ideal)"},
                    {"shape": "Oval Face", "score": "90% (Great)"},
                    {"shape": "Heart Face", "score": "88% (Great)"},
                    {"shape": "Square Face", "score": "84% (Good)"}
                ],
                "tips": [
                    "Use texturizing sea salt spray for beachy wave definition.",
                    "Opt for an off-center or side part to break symmetry.",
                    "Curtain bangs draw emphasis to eyes and cheekbones."
                ],
                "angles": [
                    {"name": "Front", "img": "/static/images/textured_bob.jpg"},
                    {"name": "Side", "img": "/static/images/bob_cut_side.jpg"},
                    {"name": "3/4 View", "img": "/static/images/bob_cut_34.jpg"},
                    {"name": "Back", "img": "/static/images/bob_cut_back.jpg"}
                ]
            },
            {
                "id": 4,
                "slug": "curly_lob",
                "name": "Voluminous Curly Lob",
                "tagline": "Springy defined curls providing vertical height.",
                "gender": "female",
                "faceshape": "round",
                "ideal_shape": "round",
                "shape_badge": "Ideal for Round Face",
                "score_badge": "93% Match",
                "main_img": "/static/images/textured_bob.jpg",
                "description": "Medium length defined curls with crown volume designed to elongate round face shapes with playful texture.",
                "hair_length": "Shoulder Length",
                "hair_texture": "Curly / Coily",
                "styling_time": "15 - 20 mins",
                "maintenance": "Moderate",
                "reasons": [
                    "Crown volume adds vertical height to round faces",
                    "Soft curls cushion jawline contours smoothly",
                    "Dynamic bouncy movement"
                ],
                "suitability": [
                    {"shape": "Round Face", "score": "93% (Ideal)"},
                    {"shape": "Oval Face", "score": "90% (Great)"}
                ],
                "tips": [
                    "Apply curl cream to soaking wet hair.",
                    "Diffuse on low heat to preserve curl pattern."
                ],
                "angles": [
                    {"name": "Front", "img": "/static/images/textured_bob.jpg"},
                    {"name": "Side", "img": "/static/images/bob_cut_side.jpg"}
                ]
            },
            {
                "id": 5,
                "slug": "layered_bob",
                "name": "Layered Soft Bob",
                "tagline": "Feathered soft layers softening strong square angles.",
                "gender": "female",
                "faceshape": "square",
                "ideal_shape": "square",
                "shape_badge": "Ideal for Square Face",
                "score_badge": "94% Match",
                "main_img": "/static/images/layered_bob.jpg",
                "description": "Feathered soft layers around the jawline designed to soften strong square angles gracefully and romantic movement.",
                "hair_length": "Past Jawline",
                "hair_texture": "Soft Layers / Waves",
                "styling_time": "10 - 15 mins",
                "maintenance": "Easy",
                "reasons": [
                    "Softens angular jawlines with romantic feathered texture",
                    "Adds gentle motion around cheekbones",
                    "Prevents blocky or boxy facial appearance",
                    "Complements side-swept bangs effortlessly"
                ],
                "suitability": [
                    {"shape": "Square Face", "score": "94% (Ideal)"},
                    {"shape": "Oval Face", "score": "91% (Great)"},
                    {"shape": "Heart Face", "score": "87% (Good)"},
                    {"shape": "Round Face", "score": "82% (Good)"}
                ],
                "tips": [
                    "Style with inward curving ends to hug the jawline.",
                    "Side-swept bangs complement feathered layers.",
                    "Incorporate subtle highlights for soft multi-dimensional texture."
                ],
                "angles": [
                    {"name": "Front", "img": "/static/images/layered_bob.jpg"},
                    {"name": "Side", "img": "/static/images/bob_cut_side.jpg"},
                    {"name": "3/4 View", "img": "/static/images/bob_cut_34.jpg"},
                    {"name": "Back", "img": "/static/images/bob_cut_back.jpg"}
                ]
            },
            {
                "id": 6,
                "slug": "french_bob",
                "name": "French A-Line Bob",
                "tagline": "Chic French cut with soft chin volume.",
                "gender": "female",
                "faceshape": "heart",
                "ideal_shape": "heart",
                "shape_badge": "Ideal for Heart Face",
                "score_badge": "96% Match",
                "main_img": "/static/images/french_bob.jpg",
                "description": "Chic French cut with soft chin fullness to balance forehead width and petite chin lines with Parisian elegance.",
                "hair_length": "Jaw Length",
                "hair_texture": "Straight or Soft Curl",
                "styling_time": "10 mins",
                "maintenance": "Easy",
                "reasons": [
                    "Adds subtle chin-level fullness to balance forehead width",
                    "Wispy Parisian bangs minimize broad hairline",
                    "Highlights cheekbones with high-fashion silhouette",
                    "Sophisticated and easy daily styling"
                ],
                "suitability": [
                    {"shape": "Heart Face", "score": "96% (Ideal)"},
                    {"shape": "Oval Face", "score": "93% (Great)"},
                    {"shape": "Round Face", "score": "85% (Good)"},
                    {"shape": "Square Face", "score": "81% (Moderate)"}
                ],
                "tips": [
                    "Inward curled ends bring weight right where your chin needs it.",
                    "Wispy full bangs disguise a wider hairline.",
                    "Keep crown volume subtle so top doesn't look top-heavy."
                ],
                "angles": [
                    {"name": "Front", "img": "/static/images/french_bob.jpg"},
                    {"name": "Side", "img": "/static/images/bob_cut_side.jpg"},
                    {"name": "3/4 View", "img": "/static/images/bob_cut_34.jpg"},
                    {"name": "Back", "img": "/static/images/bob_cut_back.jpg"}
                ]
            },
            {
                "id": 7,
                "slug": "pixie_cut",
                "name": "Chic Textured Pixie Cut",
                "tagline": "Petite cropped cut drawing emphasis to eyes & cheekbones.",
                "gender": "female",
                "faceshape": "heart",
                "ideal_shape": "heart",
                "shape_badge": "Ideal for Heart Face",
                "score_badge": "95% Match",
                "main_img": "/static/images/french_bob.jpg",
                "description": "A chic short pixie cut with piecey top texture that draws emphasis upward to eyes and cheekbones.",
                "hair_length": "Very Short",
                "hair_texture": "Textured",
                "styling_time": "5 mins",
                "maintenance": "Low",
                "reasons": [
                    "Frames heart-shaped foreheads with soft piecey fringe",
                    "Draws focus to cheekbones and delicate jawline",
                    "Ultra-fast 5-minute daily styling routine"
                ],
                "suitability": [
                    {"shape": "Heart Face", "score": "95% (Ideal)"},
                    {"shape": "Oval Face", "score": "92% (Great)"}
                ],
                "tips": [
                    "Use a pea-sized amount of styling pomade for piecey definition."
                ],
                "angles": [
                    {"name": "Front", "img": "/static/images/french_bob.jpg"}
                ]
            },

            # --- MALE HAIRSTYLES ---
            {
                "id": 8,
                "slug": "male_crop",
                "name": "Textured Crop Fade",
                "tagline": "Clean side taper paired with textured top volume.",
                "gender": "male",
                "faceshape": "oval",
                "ideal_shape": "oval",
                "shape_badge": "Ideal for Oval Face",
                "score_badge": "97% Match",
                "main_img": "/static/images/male_crop.jpg",
                "description": "Short textured top paired with clean tapered side fade that highlights natural male jawlines with crisp definition.",
                "hair_length": "Short Fade",
                "hair_texture": "Textured Crop",
                "styling_time": "5 mins",
                "maintenance": "Low",
                "reasons": [
                    "Clean side taper accentuates natural male jawlines",
                    "Textured top provides lightweight crown height",
                    "Versatile athletic and professional appearance",
                    "Quick 5-minute styling with matte clay"
                ],
                "suitability": [
                    {"shape": "Oval Face", "score": "97% (Ideal)"},
                    {"shape": "Round Face", "score": "94% (Great)"},
                    {"shape": "Square Face", "score": "90% (Great)"},
                    {"shape": "Heart Face", "score": "88% (Good)"}
                ],
                "tips": [
                    "Apply matte clay or styling paste for natural texture.",
                    "Blow dry upward at the roots for lightweight volume.",
                    "Keep side tapers clean for sharp contrast."
                ],
                "angles": [
                    {"name": "Front", "img": "/static/images/male_crop.jpg"},
                    {"name": "Side", "img": "/static/images/male_crop.jpg"},
                    {"name": "3/4 View", "img": "/static/images/male_crop.jpg"},
                    {"name": "Back", "img": "/static/images/male_crop.jpg"}
                ]
            },
            {
                "id": 9,
                "slug": "male_pompadour",
                "name": "Modern Slick Pompadour",
                "tagline": "Sleek swept-back top accentuating oval face structure.",
                "gender": "male",
                "faceshape": "oval",
                "ideal_shape": "oval",
                "shape_badge": "Ideal for Oval Face",
                "score_badge": "95% Match",
                "main_img": "/static/images/male_side_part.jpg",
                "description": "Swept-back voluminous top with clean tapered sides framing oval masculine facial proportions.",
                "hair_length": "Medium Top, Short Sides",
                "hair_texture": "Sleek Pompadour",
                "styling_time": "10 mins",
                "maintenance": "Easy",
                "reasons": [
                    "High swept top compliments oval facial balance",
                    "Clean tapered sides keep focus on eyes and brow line",
                    "Polished high-end aesthetic"
                ],
                "suitability": [
                    {"shape": "Oval Face", "score": "95% (Ideal)"},
                    {"shape": "Square Face", "score": "91% (Great)"}
                ],
                "tips": [
                    "Blow dry backward using a round brush before applying pomade."
                ],
                "angles": [
                    {"name": "Front", "img": "/static/images/male_side_part.jpg"}
                ]
            },
            {
                "id": 10,
                "slug": "male_quiff",
                "name": "High Skin Fade Quiff",
                "tagline": "Adds height & sharp side angles for round faces.",
                "gender": "male",
                "faceshape": "round",
                "ideal_shape": "round",
                "shape_badge": "Ideal for Round Face",
                "score_badge": "94% Match",
                "main_img": "/static/images/male_crop.jpg",
                "description": "A high skin fade paired with a swept-up quiff creates vertical height and sharp side contrast to visually slim round male faces.",
                "hair_length": "Medium Top, High Fade",
                "hair_texture": "Voluminous Quiff",
                "styling_time": "8 mins",
                "maintenance": "Moderate",
                "reasons": [
                    "Adds vertical height to elongate facial proportions",
                    "High fade removes side bulk to sharpen cheek lines",
                    "Swept quiff creates dynamic angular shape"
                ],
                "suitability": [
                    {"shape": "Round Face", "score": "94% (Ideal)"},
                    {"shape": "Oval Face", "score": "91% (Great)"}
                ],
                "tips": [
                    "Use a round brush while blow-drying for quiff height."
                ],
                "angles": [
                    {"name": "Front", "img": "/static/images/male_crop.jpg"}
                ]
            },
            {
                "id": 11,
                "slug": "male_side_part",
                "name": "Classic Side Part",
                "tagline": "Sleek masculine side part with subtle taper.",
                "gender": "male",
                "faceshape": "square",
                "ideal_shape": "square",
                "shape_badge": "Ideal for Square Face",
                "score_badge": "96% Match",
                "main_img": "/static/images/male_side_part.jpg",
                "description": "Refined side part with subtle taper accentuating masculine jawlines for professional polish and executive flair.",
                "hair_length": "Short/Medium",
                "hair_texture": "Sleek Side Part",
                "styling_time": "5 - 10 mins",
                "maintenance": "Easy",
                "reasons": [
                    "Highlights strong masculine jawlines and forehead symmetry",
                    "Executive polished look for professional environments",
                    "Subtle tapered sides prevent bulky width",
                    "Effortless comb styling in under 5 minutes"
                ],
                "suitability": [
                    {"shape": "Square Face", "score": "96% (Ideal)"},
                    {"shape": "Oval Face", "score": "94% (Great)"},
                    {"shape": "Round Face", "score": "89% (Good)"},
                    {"shape": "Heart Face", "score": "86% (Good)"}
                ],
                "tips": [
                    "Comb hair along natural side part while damp.",
                    "Use medium-shine pomade for a polished finish.",
                    "Keep neckline neatly trimmed."
                ],
                "angles": [
                    {"name": "Front", "img": "/static/images/male_side_part.jpg"},
                    {"name": "Side", "img": "/static/images/male_side_part.jpg"},
                    {"name": "3/4 View", "img": "/static/images/male_side_part.jpg"},
                    {"name": "Back", "img": "/static/images/male_side_part.jpg"}
                ]
            },
            {
                "id": 12,
                "slug": "male_undercut",
                "name": "Disconnected Undercut",
                "tagline": "Sharp contrast sides highlighting strong jaw symmetry.",
                "gender": "male",
                "faceshape": "square",
                "ideal_shape": "square",
                "shape_badge": "Ideal for Square Face",
                "score_badge": "95% Match",
                "main_img": "/static/images/male_side_part.jpg",
                "description": "Disconnected undercut with longer top combed over, accentuating square angular jawlines with sharp modern contrast.",
                "hair_length": "Longer Top, Undercut Sides",
                "hair_texture": "Straight / Slicked",
                "styling_time": "5 - 10 mins",
                "maintenance": "Easy",
                "reasons": [
                    "Accentuates masculine angular jawlines with high contrast",
                    "Modern edgy profile popular in mens hair fashion",
                    "Very easy side comb control"
                ],
                "suitability": [
                    {"shape": "Square Face", "score": "95% (Ideal)"},
                    {"shape": "Oval Face", "score": "92% (Great)"}
                ],
                "tips": [
                    "Use strong hold wax to keep top swept to one side."
                ],
                "angles": [
                    {"name": "Front", "img": "/static/images/male_side_part.jpg"}
                ]
            },
            {
                "id": 13,
                "slug": "male_fringe",
                "name": "Textured Forward Fringe Cut",
                "tagline": "Balances forehead width & narrow chin lines.",
                "gender": "male",
                "faceshape": "heart",
                "ideal_shape": "heart",
                "shape_badge": "Ideal for Heart Face",
                "score_badge": "93% Match",
                "main_img": "/static/images/male_crop.jpg",
                "description": "A textured forward fringe softens a wider forehead while maintaining soft side volume to balance a narrower chin.",
                "hair_length": "Medium Fringe",
                "hair_texture": "Textured / Layers",
                "styling_time": "5 mins",
                "maintenance": "Easy",
                "reasons": [
                    "Forward fringe disguises wider hairline",
                    "Textured layers add soft volume around temples",
                    "Balances forehead to chin proportion effortlessly"
                ],
                "suitability": [
                    {"shape": "Heart Face", "score": "93% (Ideal)"},
                    {"shape": "Oval Face", "score": "90% (Great)"}
                ],
                "tips": [
                    "Style fringe forward with light sea salt spray."
                ],
                "angles": [
                    {"name": "Front", "img": "/static/images/male_crop.jpg"}
                ]
            }
        ]
        self._analysis_logs = []

    def get_all_hairstyles(self, gender=None, shape=None, search=None):
        results = self._hairstyles[:]

        if gender and gender != 'all':
            results = [item for item in results if item["gender"] == gender]

        if shape and shape != 'all':
            results = [item for item in results if item["faceshape"] == shape or item["ideal_shape"] == shape]

        if search:
            search_str = search.lower()
            results = [item for item in results if search_str in item["name"].lower()]

        return results

    def get_hairstyle_by_slug(self, slug):
        for item in self._hairstyles:
            if item["slug"] == slug:
                return item
        return None

    def get_recommendation_by_shape_and_gender(self, gender, shape):
        # 1. Exact match by gender & faceshape
        for item in self._hairstyles:
            if item["gender"] == gender and (item["faceshape"] == shape or item["ideal_shape"] == shape):
                return item

        # 2. Fallback to gender match
        for item in self._hairstyles:
            if item["gender"] == gender:
                return item

        # 3. Default first item
        return self._hairstyles[0] if self._hairstyles else None

    def get_related_hairstyles(self, gender=None, shape=None, current_slug=None, limit=6):
        # 1. Primary matching by gender and faceshape (excluding current_slug)
        primary_matches = []
        for item in self._hairstyles:
            if current_slug and item["slug"] == current_slug:
                continue
            if gender and gender != 'all' and item["gender"] != gender:
                continue
            if shape and shape != 'all' and (item["faceshape"] == shape or item["ideal_shape"] == shape):
                primary_matches.append(item)

        if len(primary_matches) >= limit:
            return primary_matches[:limit]

        # 2. Backfill with same gender if needed
        fetched_slugs = [item["slug"] for item in primary_matches]
        if current_slug:
            fetched_slugs.append(current_slug)

        backfill_matches = []
        for item in self._hairstyles:
            if item["slug"] in fetched_slugs:
                continue
            if gender and gender != 'all' and item["gender"] != gender:
                continue
            backfill_matches.append(item)

        combined = primary_matches + backfill_matches
        return combined[:limit]

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
