from flask import json
import os
import time
import base64
from flask import Flask, render_template, request, jsonify, url_for
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
    # Don't pre-fetch all styles, let the JS handle fetching with pagination
    return render_template('hairstyles.html', selected_gender=gender, selected_shape=shape, selected_category=category, search=search)

@app.route('/hairstyle-detail')
def hairstyle_detail():
    style_id = request.args.get('style', 'classic_bob')
    gender = request.args.get('gender', 'female')
    style_data = hairstyle_service.get_hairstyle_by_slug(style_id)
    return render_template('hairstyle_detail.html', style_id=style_id, gender=gender, style_data=style_data)

@app.route('/color-analysis')
def color_analysis():
    gender = request.args.get('gender', 'female')
    user_img = request.args.get('user_img', '')
    undertone_raw = request.args.get('undertone', 'warm').lower()

    # Load palette from JSON file
    palette_file = os.path.join(app.root_path, 'palettes.json')
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

    return render_template(
        'color_result.html',
        image_url=user_img,
        color_type=key.upper(),
        confidence_score="96%",
        palette=recommendations.get('recommended_colors', []),
        avoid_colors=recommendations.get('avoid_colors', []),
        neutral_colors=recommendations.get('neutral_colors_that_flatter', []),
        hair_colors=recommendations.get('hair_colors', []),
        jewelry=recommendations.get('jewelry', [])
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
    """Handle image uploads, process AI analysis, and render results page."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    gender = request.form.get('gender', 'Female')
    analysis_type = request.form.get('analysis_type', 'color')  # 'color' သို့မဟုတ် 'hairstyle' ရယူခြင်း

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Generate web-accessible URL for the uploaded photo
        user_image_url = url_for('static', filename=f'uploads/{filename}')

        # -------------------------------------------------------------
        # Connect to your team's AI backend modules here
        # -------------------------------------------------------------
        # 1. Detect Skin Regions (Cheek, Forehead, Chin)
        # regions = skin_detector.extract_skin_regions(filepath) if skin_detector else None

        # 2. Classify Face Shape & Skin Tone
        # face_shape = shape_classifier.classify_face_shape(filepath) if shape_classifier else 'Round'
        # skin_tone = tone_classifier.classify_skin_tone(regions) if tone_classifier else 'Cool'

        # 3. Get Recommendations
        # hairstyles = hair_recommender.recommend_hairstyles(face_shape, gender) if hair_recommender else []
        # palette = color_recommender.recommend_color_palette(skin_tone) if color_recommender else []
        # -------------------------------------------------------------
        undertone = 'warm'
        confidence_val = 0.90
        recommendations = {}

        if skin_tone_service:
            analysis_res = skin_tone_service.analyze_image(filepath)
            if analysis_res.get("status") == "success":
                undertone = analysis_res.get("undertone", "warm")
                confidence_val = analysis_res.get("confidence", 0.90)
                recommendations = analysis_res.get("recommendations", {})
            elif get_recommendations:
                recommendations = get_recommendations(undertone)

        color_type = undertone.upper()
        confidence_score = f"{int(confidence_val * 100)}%"
        # Dynamic sample data formatted for result templates
        face_shape = "oval"
        face_shape_confidence = 0.0

        if face_shape_classifier and os.path.exists(filepath):
            shape_result = face_shape_classifier.classify(filepath)

        if "error" in shape_result:
            print(f"[FaceShapeClassifier] {shape_result['error']}")
        else:
            face_shape = shape_result["face_shape"].lower()
            face_shape_confidence = shape_result["confidence"]
        # color_type = 'COOL'
        # confidence_score = '92%'
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

        palette = recommendations.get('recommended_colors', [
            {'name': 'Navy Blue', 'hex': '#000080'},
            {'name': 'Lavender', 'hex': '#E6E6FA'},
            {'name': 'Emerald Green', 'hex': '#50C878'},
            {'name': 'Rose Pink', 'hex': '#FF66CC'},
            {'name': 'Ice Blue', 'hex': '#99FFFF'},
            {'name': 'White', 'hex': '#FFFFFF'}
        ])

        # Choose Color Analysis ခလုတ်မှ လာပါက color_result.html ကို ပြသခြင်း
        if analysis_type == 'color':
            return render_template(
                'color_result.html',
                image_url=user_image_url,
                color_type=color_type,
                confidence_score=confidence_score,
                palette=palette,
                avoid_colors=recommendations.get('avoid_colors', []),
                neutral_colors=recommendations.get('neutral_colors', []),
                hair_colors=recommendations.get('hair_colors', []),
                jewelry=recommendations.get('jewelry', [])
        )

        # Hairstyle Analysis ခလုတ်မှ လာပါက result.html ကို ပြသခြင်း
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

if __name__ == '__main__':
    app.run(debug=True, port=5000)
