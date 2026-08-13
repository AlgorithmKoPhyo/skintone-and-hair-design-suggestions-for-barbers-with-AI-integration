import os
import time
import base64
from flask import Flask, render_template, request, jsonify, url_for
from werkzeug.utils import secure_filename
from app.services.hairstyle_service import HairstyleService

# Import modules as whole packages to avoid specific function name errors
try:
    import modules.face_shape_classifier as shape_classifier
    import modules.hairstyle_recommender as hair_recommender
    import modules.color_analysis_recommender as color_recommender
    from modules.skin_tone_service import SkinToneService
    from modules.color_analysis_recommender import get_recommendations
<<<<<<< Updated upstream
except ImportError:
    # Graceful fallback if module files aren't in place yet
=======
    from modules.face_shape_classifier import FaceShapeClassifier
    from modules.face_shape_classification.src.validation.facevalidator import FaceValidator
except ImportError as e:
>>>>>>> Stashed changes
    skin_detector = None
    shape_classifier = None
    tone_classifier = None
    hair_recommender = None
    color_recommender = None
<<<<<<< Updated upstream
=======
    FaceShapeClassifier = None
    FaceValidator = None
    SkinToneService = None 
>>>>>>> Stashed changes


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
    rec_data = hairstyle_service.get_recommendation(gender=gender, shape=shape)
    current_slug = rec_data.get('slug') if rec_data else None
    related_styles = hairstyle_service.get_related_hairstyles(gender=gender, shape=shape, current_slug=current_slug, limit=6)
    return render_template('recommendation.html', gender=gender, shape=shape, user_img=user_img, rec_data=rec_data, related_styles=related_styles)

@app.route('/hairstyles')
def hairstyles():
    gender = request.args.get('gender', 'all')
    shape = request.args.get('shape', 'all')
    search = request.args.get('search', '')
    all_styles = hairstyle_service.get_all_hairstyles(gender=gender, shape=shape, search=search)
    return render_template('hairstyles.html', hairstyles=all_styles, selected_gender=gender, selected_shape=shape, search=search)

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
    gender = request.args.get('gender')
    shape = request.args.get('shape')
    search = request.args.get('search')
    styles = hairstyle_service.get_all_hairstyles(gender=gender, shape=shape, search=search)
    return jsonify({"status": "success", "data": styles})

@app.route('/api/recommendation', methods=['GET'])
def api_recommendation():
    gender = request.args.get('gender', 'female')
    shape = request.args.get('shape', 'oval')
    rec_data = hairstyle_service.get_recommendation(gender=gender, shape=shape)
    current_slug = rec_data.get('slug') if rec_data else None
    related_styles = hairstyle_service.get_related_hairstyles(gender=gender, shape=shape, current_slug=current_slug, limit=6)
    return jsonify({"status": "success", "data": rec_data, "related_styles": related_styles})

@app.route('/api/analyze', methods=['POST'])
def analyze():
    gender        = request.form.get('gender', 'female')
    analysis_type = request.form.get('analysis_type', 'hairstyle')

    # ── Save uploaded image ─────────────────────────────────────────────────
    timestamp = int(time.time())
    filename  = f"user_photo_{timestamp}.jpg"
    filepath  = os.path.join(UPLOAD_FOLDER, filename)
    saved_url = f"/static/uploads/{filename}"

    if 'image' in request.files and request.files['image'].filename != '':
        request.files['image'].save(filepath)
    elif 'image_base64' in request.form and request.form['image_base64'].strip():
        base64_data = request.form['image_base64']
        if ',' in base64_data:
            base64_data = base64_data.split(',')[1]
        try:
            with open(filepath, 'wb') as f:
                f.write(base64.b64decode(base64_data))
        except Exception as e:
            print("Error decoding base64 image:", e)
            saved_url = ''
    else:
        saved_url = ''

    # ── AI Face Shape Detection (STUB — replace with real model) ───────────
    # TODO: Replace this block with the actual face_shape_classifier module.
    # The classifier should accept `filepath` and return:
    #   detected_shape : str  — one of "oval", "round", "square", "heart"
    #   confidence     : float — 0.0 to 1.0
    #
    # Example integration once model is ready:
    #   from modules.face_shape_classifier import FaceShapeClassifier
    #   classifier = FaceShapeClassifier()
    #   detected_shape, confidence = classifier.predict(filepath)
    #
    detected_shape = "oval"   # ← stub: replace with classifier output
    confidence     = 0.96     # ← stub: replace with classifier confidence

    # ── AI Skin Tone Detection (STUB — replace with real model) ────────────
    # TODO: Replace with skin_tone_classifier module.
    # from modules.skin_tone_classifier import SkinToneClassifier
    # undertone = SkinToneClassifier().predict(filepath)
    undertone = "Warm Autumn"  # ← stub
    if skin_tone_service and os.path.exists(filepath):
        analysis_res = skin_tone_service.analyze_image(filepath)
        if analysis_res.get("status") == "success":
            undertone = analysis_res.get("undertone", "warm")

    # ── Log analysis session ────────────────────────────────────────────────
    hairstyle_service.log_user_analysis(
        user_image_url=saved_url,
        detected_shape=detected_shape,
        gender=gender,
        analysis_type=analysis_type,
        confidence=confidence
    )

    # ── Build redirect URL ──────────────────────────────────────────────────
    if analysis_type == 'hairstyle':
        redirect_url = (
            f"/recommendation?user_img={saved_url}"
            f"&shape={detected_shape}&gender={gender}"
        )
    else:
        redirect_url = (
            f"/color-analysis?user_img={saved_url}"
            f"&undertone={undertone}&gender={gender}"
        )

    return jsonify({
        "status":             "success",
        "detected_face_shape": detected_shape,
        "face_shape_title":    detected_shape.capitalize() + " Face",
        "undertone":           undertone,
        "confidence":          confidence,
        "user_image_url":      saved_url,
        "gender":              gender,
        "analysis_type":       analysis_type,
        "redirect_url":        redirect_url
    })


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
<<<<<<< Updated upstream
        face_shape = 'Round'
=======
        # face_shape = "oval"
        # face_shape_confidence = 0.0

        # if face_shape_classifier and os.path.exists(filepath):
        #     shape_result = face_shape_classifier.classify(filepath)

        # if "error" in shape_result:
        #     print(f"[FaceShapeClassifier] {shape_result['error']}")
        # else:
        #     face_shape = shape_result["face_shape"].lower()
        #     face_shape_confidence = shape_result["confidence"]
        face_shape = "oval"
        face_shape_confidence = 0.0

        if face_shape_classifier and os.path.exists(filepath):
            shape_result = face_shape_classifier.classify(filepath)

            # INDENT THESE LINES so they only run if shape_result exists
            if "error" in shape_result:
                print(f"[FaceShapeClassifier] {shape_result['error']}")
            else:
                face_shape = shape_result["face_shape"].lower()
                face_shape_confidence = shape_result["confidence"]
>>>>>>> Stashed changes
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
            skin_tone=color_type,
            gender=gender,
            hairstyles=hairstyles,
            palette=palette
        )


if __name__ == '__main__':
    app.run(debug=True, port=5000)