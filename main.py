from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from image_processing.process import process_image

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        try:
            file = request.files['file']
            if file.filename == '':
                return "No selected file", 400
            
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Debug log
            print(f"File saved to {filepath}")

            # Process the image and get the result
            result = process_image(filepath)
            print(f"Processing result: {result}")

            return render_template('index.html', fileGambar=True, result=result)
        except Exception as e:
            print(f"An error occurred: {e}")
            return "An error occurred while processing the file", 500

if __name__ == '__main__':
    app.run(debug=True)
