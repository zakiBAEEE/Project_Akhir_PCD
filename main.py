
import os
from flask import Flask, request, render_template

app = Flask(__name__)

# Tentukan direktori tempat gambar akan disimpan
UPLOAD_FOLDER = 'uploads'
# Pastikan direktori tersebut ada, jika tidak, buat direktori baru
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return 'No file part'
    file = request.files['image']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return render_template('upload_succes.html', filename=filename)

if __name__ == '__main__':
    app.run(debug=True)
