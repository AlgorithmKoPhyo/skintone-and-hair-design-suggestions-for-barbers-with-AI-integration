from flask import Flask, jsonify, render_template, request

app = Flask(__name__, template_folder='app/templates')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result')
def result():
    return render_template('result.html')


if __name__ == '__main__':
    app.run(debug=True)
