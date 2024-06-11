from flask import Flask, request, render_template
from image_processing.process import process_image

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['GET','POST'] )
def upload():
 file = request.files.get('image')
 return render_template('index.html', fileGambar=file)

if __name__ == '__main__':
    app.run(debug=True)
