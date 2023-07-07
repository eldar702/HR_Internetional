from flask import Flask, request, render_template, redirect
from werkzeug.utils import secure_filename
import os
import parse
import highlight
import visualization
import pickle

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

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

@app.route('/upload', methods=['POST'])
def upload():
    if 'resume' in request.files:
        resume = request.files['resume']
        filename = secure_filename(resume.filename)
        resume.save(os.path.join('uploads', filename))
        # Todo: add the code that should run when the submit button is clicked
        parse.process_file(filename)
        return redirect('/')  # Redirect to the home page after processing the file
    else:
        return 'No file uploaded!', 400

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