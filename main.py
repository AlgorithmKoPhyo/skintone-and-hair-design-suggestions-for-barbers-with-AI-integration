import os
from flask import Flask, render_template, request, jsonify, url_for
from werkzeug.utils import secure_filename

# Import modules as whole packages to avoid specific function name errors
try:
    import modules.skin_region_detector as skin_detector
    import modules.face_shape_classifier as shape_classifier
    import modules.skin_tone_classifier as tone_classifier
    import modules.hairstyle_recommender as hair_recommender
    import modules.color_analysis_recommender as color_recommender
except ImportError:
    # Graceful fallback if module files aren't in place yet
    skin_detector = None
    shape_classifier = None
    tone_classifier = None
    hair_recommender = None
    color_recommender = None


app = Flask(
    __name__,
    template_folder='app/templates',
    static_folder='app/static'
)

# Configuration for uploads inside app/static to allow direct web serving
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'app', 'static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max limit

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/')
def index():
    """Render the main UI page."""
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
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

        # Dynamic sample data formatted for result templates
        face_shape = 'Round'
        color_type = 'COOL'
        confidence_score = '92%'

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

        palette = [
            {'name': 'Navy Blue', 'hex': '#000080'},
            {'name': 'Lavender', 'hex': '#E6E6FA'},
            {'name': 'Emerald Green', 'hex': '#50C878'},
            {'name': 'Rose Pink', 'hex': '#FF66CC'},
            {'name': 'Ice Blue', 'hex': '#99FFFF'},
            {'name': 'White', 'hex': '#FFFFFF'}
        ]

        # Choose Color Analysis ခလုတ်မှ လာပါက color_result.html ကို ပြသခြင်း
        if analysis_type == 'color':
            return render_template(
                'color_result.html',
                image_url=user_image_url,
                color_type=color_type,
                confidence_score=confidence_score,
                palette=palette
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