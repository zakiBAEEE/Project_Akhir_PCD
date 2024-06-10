
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return 'No file part'
    file = request.form.get('image')
    return render_template('upload_success.html', fileGambar = file)

if __name__ == '__main__':
    app.run(debug=True)
