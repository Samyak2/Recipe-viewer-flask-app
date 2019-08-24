from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

import sys
import os
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from database_setup import Base, Recipe, Image, Ingredient, Step
# from flask_sqlalchemy import SQLAlchemy
from werkzeug import secure_filename
from dotenv import load_dotenv
load_dotenv()
import pyrebase
import base64
import pickle

#Connect to Database and create database session
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
# db = SQLAlchemy(app)
app.jinja_env.globals['base64'] = base64
app.jinja_env.globals['pickle'] = pickle
# engine = create_engine('sqlite:///books-collection.db')
# Base.metadata.bind = engine

config = {
  "apiKey": os.environ['FIREBASE_API_KEY'],
  "authDomain": "recipe-viewer-1.firebaseapp.com",
  "databaseURL": "https://recipe-viewer-1.firebaseio.com",
  "projectId": "recipe-viewer-1",
  "storageBucket": "recipe-viewer-1.appspot.com",
  "serviceAccount": "firebase-private-key.json",
  "messagingSenderId": "374628466588"
}
firebase = pyrebase.initialize_app(config)
firedb = firebase.database()
# firedb.child("test").push("Hmmm")

# DBSession = sessionmaker(bind=engine)
# session = DBSession()

#landing page that will display all the books in our database
#This function operate on the Read operation.
@app.route('/books')
def showBooks():
#    books = db.session.query(Recipe).all()
   vals = firedb.child("recipes").get().val()
#    print(vals)
   return render_template("books.html", recipes=vals)

#This will let us Create a new book and save it in our database
@app.route('/books/new/',methods=['GET','POST'])
def newBook():
    if request.method == 'POST':
        title = request.form["name"]
        # newRecipe = Recipe(title = title)
        newRecipedict = {"title": title}
        # images = []
        # filenames = []
        newRecipedict["filename"] = []
        newRecipedict["images"] = []
        for f in request.files.getlist("file"):
            img_encoded = base64.b64encode(f.read())
            # images.append(Image(filename=secure_filename(f.filename), image=img_encoded))
            newRecipedict["filename"].append(secure_filename(f.filename))
            newRecipedict["images"].append(img_encoded.decode("utf-8"))
            # print(image, "Hmmmmmmmmm", file=sys.stderr)
            # filenames.append(secure_filename(f.filename))
        # print(image, "Hmmmmmmmmm", file=sys.stderr)
        # newRecipe.filenames = filenames
        # images = pickle.dumps(image)
        # newRecipe.images = images
        # newRecipe.ingredients = [Ingredient(ingredient=i) for i in request.form["ingredients"].split(",")]
        newRecipedict["ingredients"] = request.form["ingredients"].split(",")
        # newRecipe.steps = [Step(step=i) for i in request.form["steps"].split(",")]
        newRecipedict["steps"] = request.form["steps"].split(",")
        # newRecipe = Recipe(title = title, filenames = filenames, image = image, ingredients = ingredients, steps = steps)
        # newRecipedict = {"title": title, "filenames": filenames, "image": image, "ingredients": ingredients, "steps": steps}
        firedb.child("recipes").push(newRecipedict)
    #    newBook = Book(title = request.form['name'], author = request.form['author'], genre = request.form['genre'])
        # db.session.add(newRecipe)
        # db.session.commit()
        # return render_template('newBook.html')
        return redirect(url_for('showBooks'))
    else:
        return render_template('newBook.html')


# #This will let us Update our books and save it in our database
# @app.route("/books/<int:book_id>/edit/", methods = ['GET', 'POST'])
# def editBook(book_id):
#    editedBook = db.session.query(Book).filter_by(id=book_id).one()
#    if request.method == 'POST':
#        if request.form['name']:
#            editedBook.title = request.form['name']
#            db.session.add(editedBook)
#            db.session.commit()
#            return redirect(url_for('showBooks'))
#    else:
#        return render_template('editBook.html', book = editedBook)

# #This will let us Delete our book
# @app.route('/books/<int:book_id>/delete/', methods = ['GET','POST'])
# def deleteBook(book_id):
#    bookToDelete = db.session.query(Book).filter_by(id=book_id).one()
#    if request.method == 'POST':
#        db.session.delete(bookToDelete)
#        db.session.commit()
#        return redirect(url_for('showBooks', book_id=book_id))
#    else:
#        return render_template('deleteBook.html',book = bookToDelete)

# @app.route('/booksApi', methods = ['GET', 'POST'])
# def booksFunction():
#    if request.method == 'GET':
#        return get_books()
#    elif request.method == 'POST':
#        title = request.args.get('title', '')
#        author = request.args.get('author', '')
#        genre = request.args.get('genre', '')
#        return makeANewBook(title, author, genre)

# @app.route('/')
# @app.route('/booksApi/', methods = ['GET', 'PUT', 'DELETE'])
# def bookFunctionId(id):
#    if request.method == 'GET':
#        return get_book(id)
 
#    elif request.method == 'PUT':
#        title = request.args.get('title', '')
#        author = request.args.get('author', '')
#        genre = request.args.get('genre', '')
#        return updateBook(id,title, author,genre)
  
#    elif request.method == 'DELETE':
#        return deleteABook(id)

# from flask import jsonify
# def get_books():
#    books = db.session.query(Book).all()
#    return jsonify(books= [b.serialize for b in books])

# def get_book(book_id):
#    books = db.session.query(Book).filter_by(id = book_id).one()
#    return jsonify(books= books.serialize)

# def makeANewBook(title,author, genre):
#    addedbook = Book(title=title, author=author,genre=genre)
#    db.session.add(addedbook)
#    db.session.commit()
#    return jsonify(Book=addedbook.serialize)

# def updateBook(id,title,author, genre):
#    updatedBook = db.session.query(Book).filter_by(id = id).one()
#    if not title:
#        updatedBook.title = title
#    if not author:
#        updatedBook.author = author
#    if not genre:
#        updatedBook.genre = genre
#    db.session.add(updatedBook)
#    db.session.commit()
#    return 'Updated a Book with id %s' % id

# def deleteABook(id):
#    bookToDelete = db.session.query(Book).filter_by(id = id).one()
#    db.session.delete(bookToDelete)
#    db.session.commit()
#    return 'Removed Book with id %s' % id

if __name__ == '__main__':
   app.debug = True
   app.run(host='0.0.0.0')