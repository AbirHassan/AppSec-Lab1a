import os
from PIL import Image
from flask import Flask, render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__, static_folder="images")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def make_square(im, thumbnail_size=(200,200)):
        background = Image.new('RGB', thumbnail_size, "black")    
        source_image = im.convert("RGB")
        source_image.thumbnail(thumbnail_size)
        (w, h) = source_image.size
        background.paste(source_image, ((thumbnail_size[0] - w) // 2, (thumbnail_size[1] - h) // 2 ))
        return background

@app.route('/')
@app.route('/index')
def index():
    images = []
    for filename in os.listdir("images"):
        images.append(filename)
    return render_template('index.html', images=images)

@app.route('/resize', methods=['GET', 'POST'])
def resize():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for("index"))
        f = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if f.filename == '':
            flash('No selected file')
            return redirect(url_for("index"))
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            #source: https://stackoverflow.com/questions/44231209/resize-rectangular-image-to-square-keeping-ratio-and-fill-background-with-black/44231784
            file_dimension = request.form['size']
            test_image = Image.open("images/" + filename)
            img = make_square(test_image, (int(file_dimension), int(file_dimension)))
            img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            return redirect(url_for("index"))
        else:
            flash('Incorrect file')
            return redirect(url_for("index"))


if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.debug = True
    app.run()