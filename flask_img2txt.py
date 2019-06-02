#!/home/sarnayakhome/miniconda3/envs/py356/bin/python

from flask import Flask, request, render_template, send_from_directory # pylint: disable=import-error
from werkzeug import secure_filename # pylint: disable=import-error
from img2textSamarth import ocr_core
import os
import sys
# import nltk
import string
from google_images_scraper import runSpider
app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# words=[]
# urls=[]
words = dict()
filename=""
text=""
@app.route("/", methods=["GET", "POST"])
def index():
    global filename
    global text
    global words
    if request.method == "POST":
        if "file" not in request.files:
            return render_template("index.html", msg="No file selected")
        file = request.files["file"]
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        text = ocr_core(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        text = text.replace('\n', '<br>')
        words = {word:"" for word in [word.strip(string.punctuation) for word in text.replace("<br>", " ").split()]}
        print(words, file=sys.stderr)
        return render_template("index.html", msg="File uploaded successfully", extracted_text=text, img_src=os.path.join(app.config['UPLOAD_FOLDER'], filename), words=words.items())#{word:url for (word, url) in zip(words, urls)})
    elif request.method == "GET":
        word = request.args.get("word")
        if word is not None:
            runSpider(word)
            words[word] = os.path.join(app.config['UPLOAD_FOLDER'], word + " 0.jpg")
            print(words[word], file=sys.stderr)
        return render_template("index.html", words=words.items(), msg="File uploaded successfully", extracted_text=text, img_src=os.path.join(app.config['UPLOAD_FOLDER'], filename))
    else:
        return render_template("index.html")

@app.route("/static/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
if __name__ == "__main__":
    app.run(debug=True)
    # app.run()