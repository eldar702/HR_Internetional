from flask import Flask, request, render_template, redirect
from werkzeug.utils import secure_filename
import os
import parse
import highlight
import visualization
import pickle

app = Flask(__name__)

@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/highlight')
def highlight_words():
    return render_template('highlight.html')

@app.route('/visualization')
def visualization_page():
    return render_template('visualization.html')

@app.route('/prediction')
def prediction_page():
    return render_template('prediction.html')

@app.route('/predict', methods=['GET'])
def predict():
    # Load the model
    model = pickle.load(open('XGBoost_model.sav', 'rb'))

    # Assume that parsed_text is the input for your model
    parsed_text = parse.parse_resume()  # You need to implement this function

    # Make a prediction
    prediction = model.predict(parsed_text)

    # Render the prediction page with the prediction
    return render_template('prediction.html', prediction=prediction)


if __name__ == '__main__':
    app.run(debug=True)