from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
    return "<html><body><h1>Hello World</h1></body></html>"

@app.route("/hello/<name>/")
def hello(name):
    return render_template("hello.html", name=name)

@app.route("/result/<int:score>/")
def result(score):
    return render_template("hello2.html", marks=score)

@app.route("/result2/")
def result2():
    dictionary = {"phy": 60, "chem": 100, "math": 30}
    return render_template("result2.html", marks=dictionary)

@app.route("/index/")
def index2():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)