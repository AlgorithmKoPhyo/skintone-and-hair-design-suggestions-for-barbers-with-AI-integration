import os
import time
import base64
import random
from flask import Flask, render_template, request, jsonify, url_for, json, Response
from werkzeug.utils import secure_filename
from app.services.hairstyle_service import HairstyleService
from modules.vgg_face_shape_classifier import VGGFaceShapeClassifier

# Import modules as whole packages to avoid specific function name errors
try:
    import modules.face_shape_classifier as shape_classifier
    import modules.hairstyle_recommender as hair_recommender
    import modules.color_analysis_recommender as color_recommender
    from modules.skin_tone_service import SkinToneService
    from modules.color_analysis_recommender import get_recommendations
    from modules.face_shape_classifier import FaceShapeClassifier
    from modules.vgg_face_validator import VGGFaceValidator as FaceValidator
except ImportError:
    # Graceful fallback if module files aren't in place yet
    skin_detector = None
    shape_classifier = None
    tone_classifier = None
    hair_recommender = None
    color_recommender = None
    FaceShapeClassifier = None
    FaceValidator = None
    SkinToneService = None 


app = Flask(
    __name__,
    template_folder='app/templates',
    static_folder='app/static'
)

# Configuration for uploads inside app/static to allow direct web serving
UPLOAD_FOLDER = os.path.join(app.static_folder, 'uploads')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max limit

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Instantiate Service Layer (Clean Request -> Service -> DAO Architecture)
hairstyle_service = HairstyleService()
skin_tone_service = SkinToneService() if SkinToneService else None
face_shape_classifier = FaceShapeClassifier() if FaceShapeClassifier else None
face_validator = FaceValidator() if FaceValidator else None
vggface_shape_classifier = VGGFaceShapeClassifier() if VGGFaceShapeClassifier else None

# ── Helper Functions for Asset Selection (Robust Path Handling) ────────────
def select_hair_colors(hair_colors, gender):
    selected_hair_colors = []
    gender_lower = gender.lower()
    for item in hair_colors:
        images = item.get("images", {})
        image = images.get(gender_lower, images.get(gender, images.get(gender.capitalize(), "")))
        if isinstance(image, list):
            image = random.choice(image) if image else ""
        
        if image and not image.startswith('assets/'):
            image = f"assets/{image}"
            
        selected_hair_colors.append({
            "name": item.get("name", ""),
            "image": image
        })
    return selected_hair_colors


def select_jewelry_images(jewelry, gender):
    selected_jewelry = []
    gender_lower = gender.lower()
    for item in jewelry:
        images = item.get("images", {})
        gender_images = images.get(gender_lower, images.get(gender, images.get(gender.capitalize(), [])))
        
        if isinstance(gender_images, list):
            selected_image = random.choice(gender_images) if gender_images else ""
        elif isinstance(gender_images, str):
            selected_image = gender_images
        else:
            selected_image = ""
        
        # Automatically fix paths if they are stored as bare filenames in palettes.json
        if selected_image and not selected_image.startswith('assets/'):
            if not selected_image.startswith('jewelry/'):
                selected_image = f"assets/jewelry/{gender_lower}/{selected_image}"
            else:
                selected_image = f"assets/{selected_image}"
                
        selected_jewelry.append({
            "name": item.get("name", ""),
            "image": selected_image
        })
    return selected_jewelry
# ───────────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    """Render the main UI page."""
    return render_template('index.html')

@app.route('/camera')
def camera():
    return render_template('camera.html')

@app.route('/recommendation')
def recommendation():
    gender = request.args.get('gender', 'female')
    shape = request.args.get('shape', 'oval')
    user_img = request.args.get('user_img', '')

    confidence = request.args.get('confidence', '0')

    try:
        confidence = float(confidence)
    except (ValueError, TypeError):
        confidence = 0.0

    rec_data = hairstyle_service.get_recommendation(
        gender=gender,
        shape=shape
    )

    current_slug = rec_data.get('slug') if rec_data else None
    related_styles = hairstyle_service.get_related_hairstyles(gender=gender, shape=shape, current_slug=current_slug, limit=5)
    return render_template('recommendation.html', gender=gender, shape=shape, user_img=user_img, rec_data=rec_data, related_styles=related_styles, confidence=confidence)

@app.route('/hairstyles')
def hairstyles():
    gender = request.args.get('gender', 'all')
    shape = request.args.get('shape', 'all')
    category = request.args.get('category', 'all')
    search = request.args.get('search', '')
    return render_template('hairstyles.html', selected_gender=gender, selected_shape=shape, selected_category=category, search=search)

@app.route('/hairstyle-detail')
def hairstyle_detail():
    style_id = request.args.get('style', 'classic_bob')
    gender = request.args.get('gender', 'female')
    style_data = hairstyle_service.get_hairstyle_by_slug(style_id)
    return render_template('hairstyle_detail.html', style_id=style_id, gender=gender, style_data=style_data)

# @app.route('/color-analysis')
# def color_analysis():
#     gender = request.args.get('gender', 'female')
#     user_img = request.args.get('user_img', '')
#     undertone_raw = request.args.get('undertone', 'warm').lower()

#     # Load palette from JSON file
#     palette_file = os.path.join(app.root_path, 'palettes.json')
#     recommendations = {}
    
#     key = 'warm'
#     if 'cool' in undertone_raw:
#         key = 'cool'
#     elif 'neutral' in undertone_raw:
#         key = 'neutral'

#     if os.path.exists(palette_file):
#         with open(palette_file, 'r') as f:
#             all_palettes = json.load(f)
#             recommendations = all_palettes.get(key, all_palettes.get('warm', {}))

#     return render_template(
#         'color_analysis.html',
#         image_url=user_img,
#         color_type=key.upper(),
#         confidence_score="96%",
#         recommended_colors=recommendations.get('recommended_colors', []),
#         avoid_colors=recommendations.get('avoid_colors', []),
#         neutral_colors=recommendations.get('neutral_colors_that_flatter', []),
#         hair_colors=recommendations.get('hair_colors', []),
#         jewelry=recommendations.get('jewelry', []),
#         occasion_recommendations=recommendations.get('occasion_recommendations', {})
#     )
@app.route('/color-analysis')
def color_analysis():
    gender = request.args.get('gender', 'female').lower()
    user_img = request.args.get('user_img', '')
    undertone_raw = request.args.get('undertone', 'warm').lower()

    palette_file = os.path.join(app.root_path, 'modules', 'palettes.json')
    recommendations = {}
    
    key = 'warm'
    if 'cool' in undertone_raw:
        key = 'cool'
    elif 'neutral' in undertone_raw:
        key = 'neutral'

    if os.path.exists(palette_file):
        with open(palette_file, 'r') as f:
            all_palettes = json.load(f)
            recommendations = all_palettes.get(key, all_palettes.get('warm', {}))

    raw_hair_colors = recommendations.get('hair_colors', [])
    raw_jewelry = recommendations.get('jewelry', [])

    hair_colors = select_hair_colors(raw_hair_colors, gender)
    jewelry = select_jewelry_images(raw_jewelry, gender)

    return render_template(
        'color_analysis.html',
        image_url=user_img,
        color_type=key.upper(),
        confidence_score="96%",
        palette=recommendations.get('recommended_colors', []),
        avoid_colors=recommendations.get('avoid_colors', []),
        neutral_colors=recommendations.get('neutral_colors_that_flatter', []),
        hair_colors=hair_colors,
        jewelry=jewelry
    )


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/api/hairstyles', methods=['GET'])
def api_hairstyles():
    gender = request.args.get('gender', 'all')
    shape = request.args.get('shape', 'all')
    category = request.args.get('category', 'all')
    search = request.args.get('search', '')
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 12))
    
    styles = hairstyle_service.get_all_hairstyles(gender=gender, shape=shape, search=search, category=category)
    
    total = len(styles)
    start = (page - 1) * limit
    end = start + limit
    paginated_styles = styles[start:end]
    
    return jsonify({
        "status": "success", 
        "data": paginated_styles,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit
    })

@app.route('/api/recommendation', methods=['GET'])
def api_recommendation():
    gender = request.args.get('gender', 'female')
    shape = request.args.get('shape', 'oval')
    rec_data = hairstyle_service.get_recommendation(gender=gender, shape=shape)
    current_slug = rec_data.get('slug') if rec_data else None
    related_styles = hairstyle_service.get_related_hairstyles(gender=gender, shape=shape, current_slug=current_slug, limit=5)
    return jsonify({"status": "success", "data": rec_data, "related_styles": related_styles})




@app.route('/analyze', methods=['POST'])
def render_analyze_result():
    file = request.files.get('file') or request.files.get('image')
    if not file or file.filename == '':
        return jsonify({'error': 'No file uploaded'}), 400

    gender = request.form.get('gender', 'Female')
    analysis_type = request.form.get('analysis_type', 'color')

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    user_image_url = url_for('static', filename=f'uploads/{filename}')

    undertone = 'warm'
    confidence_val = 0.90
    recommendations = {}

    if skin_tone_service:
        analysis_res = skin_tone_service.analyze_image(filepath)
        if analysis_res.get("status") == "success":
            undertone = analysis_res.get("undertone", "warm")
            confidence_val = analysis_res.get("confidence", 0.90)
            recommendations = analysis_res.get("recommendations", {})

    palette_file = os.path.join(app.root_path, 'modules', 'palettes.json')
    key = 'warm'
    if 'cool' in undertone.lower():
        key = 'cool'
    elif 'neutral' in undertone.lower():
        key = 'neutral'

    json_recommendations = {}

    if os.path.exists(palette_file):
        with open(palette_file, 'r') as f:
            all_palettes = json.load(f)
            json_recommendations = all_palettes.get(key, all_palettes.get('warm', {}))
            if not recommendations.get('hair_colors'):
                recommendations['hair_colors'] = json_recommendations.get('hair_colors', [])
            if not recommendations.get('jewelry'):
                recommendations['jewelry'] = json_recommendations.get('jewelry', [])
            if not recommendations.get('recommended_colors'):
                recommendations['recommended_colors'] = json_recommendations.get('recommended_colors', [])
            if not recommendations.get('avoid_colors'):
                recommendations['avoid_colors'] = json_recommendations.get('avoid_colors', [])
            if not recommendations.get('neutral_colors_that_flatter'):
                recommendations['neutral_colors_that_flatter'] = json_recommendations.get('neutral_colors_that_flatter', [])

    color_type = undertone.upper()
    confidence_score = f"{int(confidence_val * 100)}%"
    
    face_shape = "oval"
    face_shape_confidence = 0.0

    if face_shape_classifier and os.path.exists(filepath):
        shape_result = face_shape_classifier.classify(filepath)
        if shape_result and "error" in shape_result:
            print(f"[FaceShapeClassifier] {shape_result['error']}")
        elif shape_result:
            face_shape = shape_result.get("face_shape", "oval").lower()
            face_shape_confidence = shape_result.get("confidence", 0.0)

    hairstyles = [
        {
            'name': 'Long Layered Cut',
            'match': '95% Match',
            'image_url': 'https://placehold.co/300x400/e0e0e0/333333?text=Long+Layered+Cut'
        },
        {
            'name': 'Soft Side Waves',
            'match': '91% Match',
            'image_url': 'https://placehold.co/300x400/e0e0e0/333333?text=Soft+Side+Waves'
        },
        {
            'name': 'Textured Side Bangs',
            'match': '89% Match',
            'image_url': 'https://placehold.co/300x400/e0e0e0/333333?text=Textured+Side+Bangs'
        }
    ]

    palette = recommendations.get('recommended_colors', [])
    raw_hair_colors = json_recommendations.get('hair_colors', []) if json_recommendations else recommendations.get('hair_colors', [])
    raw_jewelry = json_recommendations.get('jewelry', []) if json_recommendations else recommendations.get('jewelry', [])

    hair_colors = select_hair_colors(raw_hair_colors, gender.lower())
    jewelry = select_jewelry_images(raw_jewelry, gender.lower())

    if analysis_type == 'color':
        return render_template(
            'color_analysis.html',
            image_url=user_image_url,
            color_type=color_type,
            confidence_score=confidence_score,
            palette=palette,
            avoid_colors=recommendations.get('avoid_colors', []),
            neutral_colors=recommendations.get('neutral_colors_that_flatter', recommendations.get('neutral_colors', [])),
            hair_colors=hair_colors,
            jewelry=jewelry
        )

    return render_template(
        'result.html',
        user_image=user_image_url,
        face_shape=face_shape,
        face_shape_confidence=face_shape_confidence,
        skin_tone=color_type,
        gender=gender,
        hairstyles=hairstyles,
        palette=palette
    )




from app.controllers.analyze_controller import analyze, validate_face

app.add_url_rule('/api/analyze', view_func=analyze, methods=['POST'])
app.add_url_rule('/validate-face', view_func=validate_face, methods=['POST'])

# -------------------------------------------------------------
# Error Handlers & Testing
# -------------------------------------------------------------
@app.route('/test-500')
def test_500():
    # This route intentionally crashes to show the 500 Error Page
    from flask import abort
    abort(500)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/export-pdf', methods=['GET'])
def export_pdf():
    """Server-side PDF export using Playwright (headless Chromium).
    Example: /export-pdf?gender=female&undertone=warm&user_img=/static/uploads/you.jpg
    """
    gender = request.args.get('gender', 'female')
    undertone = request.args.get('undertone', 'warm')
    user_img = request.args.get('user_img', '')

    render_url = url_for('color_analysis', gender=gender, undertone=undertone, user_img=user_img, _external=True)

    try:
        from playwright.sync_api import sync_playwright
    except Exception:
        return jsonify({
            'status': 'error',
            'message': 'Playwright not installed. Please install and run `playwright install`.'
        }), 500

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            # Use a wide viewport to render full-width layout
            try:
                page.set_viewport_size({"width": 1800, "height": 1000})
            except Exception:
                pass
            page.goto(render_url, wait_until='networkidle')
            # Render as landscape A4 to capture horizontal layouts
            pdf_bytes = page.pdf(format='A4', landscape=True, print_background=True, margin={'top':'4mm','bottom':'4mm','left':'4mm','right':'4mm'})
            browser.close()

        return Response(pdf_bytes, mimetype='application/pdf', headers={
            'Content-Disposition': 'attachment; filename="color-analysis.pdf"'
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
