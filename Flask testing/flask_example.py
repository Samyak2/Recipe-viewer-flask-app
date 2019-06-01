from flask import Flask, redirect, url_for, request

app = Flask(__name__)
@app.route("/test/<name>/<float:num>")
def hello_world(name, num):
    return  "Hello W0rld you are number " + str(num) + " of name " + name

@app.route("/python")
def pyth():
    return "Hello python"

@app.route("/flask/")
def flas():
    return "Hello flask"

@app.route("/admin/")
def admin():
    return  "Welcome admin, you have no power here"

@app.route("/guest/<name>/")
def guest(name):
    return  "Welcome guest %s" %name

@app.route("/user/<name>/")
def user(name):
    if(name == "admin"):
        return redirect(url_for("admin"))
    else:
        return redirect(url_for("guest", name=name))

@app.route("/success/<name>")
def success(name):
    return "Welcome %s you have logged in successfully" %name

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("success", name=user))
    else:
        user = request.args.get("nm")
        return redirect(url_for("success", name=user))



# app.debug = True
if __name__ == "__main__":
    app.run(debug = True)