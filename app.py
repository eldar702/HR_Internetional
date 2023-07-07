from flask import Flask, render_template, request, redirect, session
from werkzeug.utils import secure_filename
import os

import highlight
import parse
import pickle

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
        highlighted_words = highlight.highlight_important_words(filename)
        # Pass this list to the template
        return render_template('highlight.html', highlighted_words=highlighted_words)
    else:
        return render_template('highlight.html')
@app.route('/visualization')
def visualization_page():
    return render_template('visualization.html')

@app.route('/prediction')
def prediction_page():
    return render_template('prediction.html')

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
    model = pickle.load(open('XGBoost_model.sav', 'rb'))
    parsed_text = parse.parse_resume()
    prediction = model.predict(parsed_text)
    return render_template('prediction.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)