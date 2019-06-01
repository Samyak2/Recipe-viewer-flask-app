from flask import Flask, request, render_template, send_from_directory
from werkzeug import secure_filename
from img2txt import ocr_core
import os
app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return render_template("index.html", msg="No file selected")
        file = request.files["file"]
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        text = ocr_core(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template("index.html", msg="File uploaded successfully", extracted_text=text, img_src=os.path.join(app.config['UPLOAD_FOLDER'], filename))
    else:
        return render_template("index.html")

@app.route("/static/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
if __name__ == "__main__":
    app.run(debug=True)