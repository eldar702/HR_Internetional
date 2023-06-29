from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import parse
import highlight

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join('uploads/', filename))
        parse.parse_to_csv(file)
        return redirect(url_for('highlight_words'))
    return render_template('upload.html')

@app.route('/highlight', methods=['GET', 'POST'])
def highlight_words():
    if request.method == 'POST':
        return highlight.highlight_important_words()
    return render_template('highlight.html')

@app.route('/visualization', methods=['GET', 'POST'])
def visualization():
    if request.method == 'POST':
        function_name = request.form['function_name']
        return redirect(url_for(function_name))
    return render_template('visualization.html')

if __name__ == '__main__':
    app.run(debug=True)
