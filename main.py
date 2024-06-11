from flask import Flask, request, render_template
from image_processing.process import process_image

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['GET','POST'] )
def upload():
 result = None
 file = request.files.get('image')
 if file:
    file_path = f"./static/images/{file.filename}"
    file.save(file_path)
    result = process_image(file_path)
    return render_template('index.html', fileGambar=file, hasil=result)
 return render_template('index.html', fileGambar=file, hasil=result)

if __name__ == '__main__':
    app.run(debug=True)
