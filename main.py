import os
import time
import base64
from flask import Flask, render_template, request, jsonify
from app.services.hairstyle_service import HairstyleService

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

UPLOAD_FOLDER = os.path.join(app.static_folder, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Instantiate Service Layer (Clean Request -> Service -> DAO Architecture)
hairstyle_service = HairstyleService()

@app.route('/')
def index():
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
    return render_template('color_analysis.html', gender=gender, user_img=user_img)

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



if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5050)
