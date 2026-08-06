from flask import Flask, jsonify, render_template, request
from modules.skin_tone_classifier import classify_skin_tone
from modules.color_analysis_recommender import get_recommendations

app = Flask(__name__, template_folder='app/templates')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result')
def result():
    return render_template('result.html')

@app.route("/analyze", methods=["POST"])
def analyze():

    image = request.files["image"]

    # Get undertone from skintone classifier module
    undertone = classify_skin_tone(image)

    # Example:
    # undertone = "cool"

    # Step 2: Get recommendations
    color_result = get_recommendations(undertone)

    return jsonify({
        "skin_tone": undertone,
        "color_recommendation": color_result
    })

if __name__ == '__main__':
    app.run(debug=True)
