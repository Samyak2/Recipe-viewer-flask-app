from flask import Flask, request, render_template, send_from_directory
from werkzeug import secure_filename
from img2text import ocr_core
import os
import sys
from collections import OrderedDict
from google_images_scraper import runSpider
import nltk

app = Flask(__name__) #initialize flask object
UPLOAD_FOLDER = 'static/uploads/' #folder where uploaded images are to be stored
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
nltk.data.path.append('./nltk_data/')

words = OrderedDict() #ordered dictionary to store words and corresponding image url
filename="" #to store name of uploaded image file
text="" #to store text extracted from image
@app.route("/", methods=["GET", "POST"]) #first argument is url where the page will be (relative to localhost:5000)
def index():
    global filename
    global text
    global words #use global variables
    #if image is uploaded
    if request.method == "POST":
        if "file" not in request.files: #if file is not uploaded
            return render_template("index.html", msg="No file selected") #Display message, {{msg}} in the html is replaced with the message
        file = request.files["file"] #get uploaded file
        filename = secure_filename(file.filename) #get file name
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) #save file to upload folder
        text = ocr_core(os.path.join(app.config['UPLOAD_FOLDER'], filename)) #get image text using ocr_core function from img2txt
        text = text.replace('\n', '<br>') #replace newline with <br> so that it is rendered properly in the html, also converts to lowecase
        words = OrderedDict(("".join(l for l in word if l.isalpha() or l==" "),"") for word in nltk.tokenize.sent_tokenize(text.lower().replace("<br><br>", ". ").replace("<br>", " ").replace("..",".")) if len(word)>2) #[word.strip(string.punctuation) for word in text.lower().replace("<br>", " ").split()]) #Get list of words from the text
        print(nltk.tokenize.sent_tokenize(text.lower().replace("<br><br>", ". ").replace("<br>", " ").replace("..",".")), file=sys.stderr)
        #load index.html again with the appropriate message, image source, words list
        if request.form.get("getall"):
            for word in words:
                runSpider(word) #runs google image scraper (from google_images_scraper.py) to get download the image
                words[word] = os.path.join(app.config['UPLOAD_FOLDER'], word + " 0.jpg") #add image url to the dict
                # print(words[word], file=sys.stderr)
        return render_template("index.html", msg="File uploaded successfully", extracted_text=text, img_src=os.path.join(app.config['UPLOAD_FOLDER'], filename), words=words.items())#{word:url for (word, url) in zip(words, urls)})
    #if any "Search for image button is clicked"
    elif request.method == "GET":
        word = request.args.get("word") #get word
        if word is not None: #if word is found
            runSpider(word) #runs google image scraper (from google_images_scraper.py) to get download the image
            words[word] = os.path.join(app.config['UPLOAD_FOLDER'], word + " 0.jpg") #add image url to the dict
            print(words[word], file=sys.stderr)
        #load index.html again with the appropriate message, image source, words list
        return render_template("index.html", words=words.items(), extracted_text=text, img_src=os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #when the page is first loaded
    else:
        return render_template("index.html")

#to show image
@app.route("/static/uploads/<file>")
def uploaded_file(file):
    return send_from_directory(UPLOAD_FOLDER, file) #send image

#run flask app when script is run directly
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000)) #get port number from heroku, or use 5000 if run locally
    app.run(debug=True, host='0.0.0.0', port=port)