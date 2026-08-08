# ==========================================================================
# StyleMe - Database Manager & Seed Initializer (SQLite / MySQL Ready)
# ==========================================================================
import os
import sqlite3
import json

DB_PATH = os.path.join(os.path.dirname(__file__), 'styleme.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # 1. Hairstyles Table (Includes explicit 'faceshape' column)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hairstyles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slug TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            tagline TEXT,
            gender TEXT NOT NULL,
            faceshape TEXT NOT NULL DEFAULT 'oval',
            shape_badge TEXT,
            score_badge TEXT,
            main_img TEXT NOT NULL,
            description TEXT,
            ideal_shape TEXT NOT NULL,
            hair_length TEXT,
            hair_texture TEXT,
            styling_time TEXT,
            maintenance TEXT,
            reasons_json TEXT,
            suitability_json TEXT,
            tips_json TEXT,
            angles_json TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 2. Face Shapes Classification Reference Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS face_shapes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            shape_code TEXT UNIQUE NOT NULL,
            display_title TEXT NOT NULL,
            subtitle TEXT,
            description TEXT,
            recommended_female_style_slug TEXT,
            recommended_male_style_slug TEXT
        )
    ''')

    # 3. User Photo AI Analysis Logs Table
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
    conn.close()

def seed_db():
    init_db()
    conn = get_db()
    cursor = conn.cursor()

    # Migration check for existing databases
    cursor.execute("PRAGMA table_info(hairstyles)")
    columns = [row[1] for row in cursor.fetchall()]
    if 'faceshape' not in columns:
        cursor.execute("ALTER TABLE hairstyles ADD COLUMN faceshape TEXT DEFAULT 'oval'")
    if 'reasons_json' not in columns:
        cursor.execute("ALTER TABLE hairstyles ADD COLUMN reasons_json TEXT")

    # Initial Extensive Hairstyles Seed Dataset (With explicit faceshape column mapping)
    hairstyles_seed = [
        # --- FEMALE HAIRSTYLES ---
        {
            "slug": "classic_bob",
            "name": "Classic Bob Cut",
            "tagline": "Timeless chin-length cut enhancing natural symmetry.",
            "gender": "female",
            "faceshape": "oval",
            "shape_badge": "Ideal for Oval Face",
            "score_badge": "95% Match",
            "main_img": "/static/images/classic_bob.jpg",
            "description": "Chin-length classic haircut with clean ends that frames oval faces with timeless symmetry and sophisticated balance.",
            "ideal_shape": "oval",
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
            "slug": "curtain_bangs_waves",
            "name": "Curtain Bangs & Long Waves",
            "tagline": "Soft cheekbone framing curtain bangs with flowing waves.",
            "gender": "female",
            "faceshape": "oval",
            "shape_badge": "Ideal for Oval Face",
            "score_badge": "96% Match",
            "main_img": "/static/images/hero_model.jpg",
            "description": "Soft sweeping curtain bangs paired with long cascading waves that accentuate cheekbones and natural facial balance.",
            "ideal_shape": "oval",
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
            "slug": "textured_bob",
            "name": "Textured Long Bob (Lob)",
            "tagline": "Collarbone length with subtle layers elongating face shape.",
            "gender": "female",
            "faceshape": "round",
            "shape_badge": "Ideal for Round Face",
            "score_badge": "92% Match",
            "main_img": "/static/images/textured_bob.jpg",
            "description": "Collarbone length with subtle layers that elongate round faces and soften cheek curves with light vertical body.",
            "ideal_shape": "round",
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
            "slug": "curly_lob",
            "name": "Voluminous Curly Lob",
            "tagline": "Springy defined curls providing vertical height.",
            "gender": "female",
            "faceshape": "round",
            "shape_badge": "Ideal for Round Face",
            "score_badge": "93% Match",
            "main_img": "/static/images/textured_bob.jpg",
            "description": "Medium length defined curls with crown volume designed to elongate round face shapes with playful texture.",
            "ideal_shape": "round",
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
            "slug": "layered_bob",
            "name": "Layered Soft Bob",
            "tagline": "Feathered soft layers softening strong square angles.",
            "gender": "female",
            "faceshape": "square",
            "shape_badge": "Ideal for Square Face",
            "score_badge": "94% Match",
            "main_img": "/static/images/layered_bob.jpg",
            "description": "Feathered soft layers around the jawline designed to soften strong square angles gracefully and romantic movement.",
            "ideal_shape": "square",
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
            "slug": "french_bob",
            "name": "French A-Line Bob",
            "tagline": "Chic French cut with soft chin volume.",
            "gender": "female",
            "faceshape": "heart",
            "shape_badge": "Ideal for Heart Face",
            "score_badge": "96% Match",
            "main_img": "/static/images/french_bob.jpg",
            "description": "Chic French cut with soft chin fullness to balance forehead width and petite chin lines with Parisian elegance.",
            "ideal_shape": "heart",
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
            "slug": "pixie_cut",
            "name": "Chic Textured Pixie Cut",
            "tagline": "Petite cropped cut drawing emphasis to eyes & cheekbones.",
            "gender": "female",
            "faceshape": "heart",
            "shape_badge": "Ideal for Heart Face",
            "score_badge": "95% Match",
            "main_img": "/static/images/french_bob.jpg",
            "description": "A chic short pixie cut with piecey top texture that draws emphasis upward to eyes and cheekbones.",
            "ideal_shape": "heart",
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
            "slug": "male_crop",
            "name": "Textured Crop Fade",
            "tagline": "Clean side taper paired with textured top volume.",
            "gender": "male",
            "faceshape": "oval",
            "shape_badge": "Ideal for Oval Face",
            "score_badge": "97% Match",
            "main_img": "/static/images/male_crop.jpg",
            "description": "Short textured top paired with clean tapered side fade that highlights natural male jawlines with crisp definition.",
            "ideal_shape": "oval",
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
            "slug": "male_pompadour",
            "name": "Modern Slick Pompadour",
            "tagline": "Sleek swept-back top accentuating oval face structure.",
            "gender": "male",
            "faceshape": "oval",
            "shape_badge": "Ideal for Oval Face",
            "score_badge": "95% Match",
            "main_img": "/static/images/male_side_part.jpg",
            "description": "Swept-back voluminous top with clean tapered sides framing oval masculine facial proportions.",
            "ideal_shape": "oval",
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
            "slug": "male_quiff",
            "name": "High Skin Fade Quiff",
            "tagline": "Adds height & sharp side angles for round faces.",
            "gender": "male",
            "faceshape": "round",
            "shape_badge": "Ideal for Round Face",
            "score_badge": "94% Match",
            "main_img": "/static/images/male_crop.jpg",
            "description": "A high skin fade paired with a swept-up quiff creates vertical height and sharp side contrast to visually slim round male faces.",
            "ideal_shape": "round",
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
            "slug": "male_side_part",
            "name": "Classic Side Part",
            "tagline": "Sleek masculine side part with subtle taper.",
            "gender": "male",
            "faceshape": "square",
            "shape_badge": "Ideal for Square Face",
            "score_badge": "96% Match",
            "main_img": "/static/images/male_side_part.jpg",
            "description": "Refined side part with subtle taper accentuating masculine jawlines for professional polish and executive flair.",
            "ideal_shape": "square",
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
            "slug": "male_undercut",
            "name": "Disconnected Undercut",
            "tagline": "Sharp contrast sides highlighting strong jaw symmetry.",
            "gender": "male",
            "faceshape": "square",
            "shape_badge": "Ideal for Square Face",
            "score_badge": "95% Match",
            "main_img": "/static/images/male_side_part.jpg",
            "description": "Disconnected undercut with longer top combed over, accentuating square angular jawlines with sharp modern contrast.",
            "ideal_shape": "square",
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
            "slug": "male_fringe",
            "name": "Textured Forward Fringe Cut",
            "tagline": "Balances forehead width & narrow chin lines.",
            "gender": "male",
            "faceshape": "heart",
            "shape_badge": "Ideal for Heart Face",
            "score_badge": "93% Match",
            "main_img": "/static/images/male_crop.jpg",
            "description": "A textured forward fringe softens a wider forehead while maintaining soft side volume to balance a narrower chin.",
            "ideal_shape": "heart",
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

    # Insert or update each seed hairstyle into database with faceshape column
    for item in hairstyles_seed:
        cursor.execute('''
            INSERT INTO hairstyles (
                slug, name, tagline, gender, faceshape, shape_badge, score_badge, main_img,
                description, ideal_shape, hair_length, hair_texture, styling_time, maintenance,
                reasons_json, suitability_json, tips_json, angles_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(slug) DO UPDATE SET
                name=excluded.name,
                tagline=excluded.tagline,
                gender=excluded.gender,
                faceshape=excluded.faceshape,
                shape_badge=excluded.shape_badge,
                score_badge=excluded.score_badge,
                main_img=excluded.main_img,
                description=excluded.description,
                ideal_shape=excluded.ideal_shape,
                hair_length=excluded.hair_length,
                hair_texture=excluded.hair_texture,
                styling_time=excluded.styling_time,
                maintenance=excluded.maintenance,
                reasons_json=excluded.reasons_json,
                suitability_json=excluded.suitability_json,
                tips_json=excluded.tips_json,
                angles_json=excluded.angles_json
        ''', (
            item["slug"], item["name"], item["tagline"], item["gender"], item["faceshape"], item["shape_badge"], item["score_badge"],
            item["main_img"], item["description"], item["ideal_shape"], item["hair_length"], item["hair_texture"],
            item["styling_time"], item["maintenance"], json.dumps(item["reasons"]), json.dumps(item["suitability"]),
            json.dumps(item["tips"]), json.dumps(item["angles"])
        ))

    # Face Shapes Seed Dataset
    shapes_seed = [
        ("oval", "Oval Face", "Balanced & Versatile", "Balanced facial proportions with gentle curving jawline.", "classic_bob", "male_crop"),
        ("round", "Round Face", "Soft & Symmetrical", "Equal width and height with soft jaw curve.", "textured_bob", "male_quiff"),
        ("square", "Square Face", "Defined & Angular", "Strong defined jawline with angular temple lines.", "layered_bob", "male_side_part"),
        ("heart", "Heart Face", "Wide Forehead & Petite Chin", "Wider cheekbones tapering down to a narrow chin line.", "french_bob", "male_fringe")
    ]

    for item in shapes_seed:
        cursor.execute('''
            INSERT INTO face_shapes (shape_code, display_title, subtitle, description, recommended_female_style_slug, recommended_male_style_slug)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(shape_code) DO UPDATE SET
                display_title=excluded.display_title,
                subtitle=excluded.subtitle,
                description=excluded.description,
                recommended_female_style_slug=excluded.recommended_female_style_slug,
                recommended_male_style_slug=excluded.recommended_male_style_slug
        ''', item)

    conn.commit()
    conn.close()

def get_all_hairstyles(gender=None, shape=None, search=None):
    conn = get_db()
    cursor = conn.cursor()

    query = "SELECT * FROM hairstyles WHERE 1=1"
    params = []

    if gender and gender != 'all':
        query += " AND gender = ?"
        params.append(gender)
    if shape and shape != 'all':
        query += " AND (faceshape = ? OR ideal_shape = ?)"
        params.extend([shape, shape])
    if search:
        query += " AND LOWER(name) LIKE ?"
        params.append(f"%{search.lower()}%")

    query += " ORDER BY id ASC"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [format_hairstyle_row(dict(row)) for row in rows]

def get_hairstyle_by_slug(slug):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM hairstyles WHERE slug = ?", (slug,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return format_hairstyle_row(dict(row))
    return None

def get_recommendation_by_shape_and_gender(gender, shape):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM hairstyles WHERE gender = ? AND (faceshape = ? OR ideal_shape = ?) LIMIT 1", (gender, shape, shape))
    row = cursor.fetchone()
    if not row:
        cursor.execute("SELECT * FROM hairstyles WHERE gender = ? LIMIT 1", (gender,))
        row = cursor.fetchone()
    conn.close()
    if row:
        return format_hairstyle_row(dict(row))
    return None

def get_related_hairstyles(gender=None, shape=None, current_slug=None, limit=6):
    conn = get_db()
    cursor = conn.cursor()
    
    query = "SELECT * FROM hairstyles WHERE 1=1"
    params = []

    if gender and gender != 'all':
        query += " AND gender = ?"
        params.append(gender)

    if shape and shape != 'all':
        query += " AND (faceshape = ? OR ideal_shape = ?)"
        params.extend([shape, shape])

    if current_slug:
        query += " AND slug != ?"
        params.append(current_slug)

    query += " ORDER BY id ASC LIMIT ?"
    params.append(limit)

    cursor.execute(query, params)
    rows = [dict(row) for row in cursor.fetchall()]

    # If fewer than limit results found for specific faceshape, backfill with matching gender
    if len(rows) < limit and gender and gender != 'all':
        fetched_slugs = [r['slug'] for r in rows]
        if current_slug and current_slug not in fetched_slugs:
            fetched_slugs.append(current_slug)

        needed = limit - len(rows)
        placeholders = ','.join('?' for _ in fetched_slugs) if fetched_slugs else "''"
        backfill_query = f"SELECT * FROM hairstyles WHERE gender = ? AND slug NOT IN ({placeholders}) ORDER BY id ASC LIMIT ?"
        backfill_params = [gender] + fetched_slugs + [needed]

        cursor.execute(backfill_query, backfill_params)
        backfill_rows = [dict(row) for row in cursor.fetchall()]
        rows.extend(backfill_rows)

    conn.close()
    return [format_hairstyle_row(row) for row in rows]

def format_hairstyle_row(data):
    data['reasons'] = json.loads(data['reasons_json']) if data.get('reasons_json') else [
        "Maintains natural face symmetry",
        "Frames facial features beautifully",
        "Easy to style and maintain"
    ]
    data['suitability'] = json.loads(data['suitability_json']) if data.get('suitability_json') else []
    data['tips'] = json.loads(data['tips_json']) if data.get('tips_json') else []
    data['angles'] = json.loads(data['angles_json']) if data.get('angles_json') else []
    return data

def save_analysis_log(user_image_url, detected_shape, gender, analysis_type='hairstyle', confidence=0.96):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO user_analyses (user_image_url, detected_shape, gender, analysis_type, confidence)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_image_url, detected_shape, gender, analysis_type, confidence))
    conn.commit()
    conn.close()
