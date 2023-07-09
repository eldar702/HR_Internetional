import json
from io import StringIO

import joblib
import pandas as pd
from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.utils import secure_filename
import os

import highlight
import parse
import pickle

import visualization

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/highlight', methods=['GET', 'POST'])
def highlight_route():
    if request.method == 'POST':
        # Use the filename saved in the session
        filename = session.get('filename')
        # Get the list of words to highlight
        clean_text, entities = highlight.highlight_important_words(filename)
        session['clean_text'] = clean_text
        # Pass this list to the template
        return render_template('highlight.html', clean_text=clean_text, entities=entities)
    else:
        return render_template('highlight.html')
@app.route('/visualization')
def visualization_page():
    filename = session.get('filename')
    image_path = visualization.create_visualization(filename)
    return render_template('visualization.html', image_path=image_path)

@app.route('/load_visualization')
def load_visualization():
    filename = session.get('filename')
    visualization.create_visualization(filename)
    return {"image_path": url_for('static', filename='images/sunburst.png')}




@app.route('/upload', methods=['POST'])
def upload():
    if 'resume' in request.files:
        resume = request.files['resume']
        filename = secure_filename(resume.filename)
        resume.save(os.path.join('uploads', filename))

        # Save the filename in the session
        session['filename'] = filename

        parse.process_file(filename)
        return redirect('/')  # Redirect to the home page after processing the file
    else:
        return 'No file uploaded!', 400


@app.route('/predict', methods=['GET'])
def predict():
    # Load the saved vectorizer and model
    model = joblib.load('XGBoost_model.sav.pkl')
    vectorizer = joblib.load('vectorizer.pkl')
    clean_text = session.get('clean_text')

    # Transform the new instance using the loaded vectorizer
    clean_text_df = pd.DataFrame([clean_text], columns=['text'])  # Assuming clean_text is a single string
    X_new = vectorizer.transform(clean_text_df['text'])

    # Make predictions on the new instance
    prediction = model.predict(X_new)

    label_encoder = joblib.load('label_encoder.pkl')
    prediction = label_encoder.inverse_transform([prediction])
    session['prediction'] = prediction[0]

    return redirect(url_for('prediction_page'))


@app.route('/prediction')
def prediction_page():
    prediction = session.get('prediction')
    return render_template('prediction.html', prediction=prediction)


if __name__ == '__main__':
    app.run(debug=True)