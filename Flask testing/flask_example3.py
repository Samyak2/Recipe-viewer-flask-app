from flask import Flask, request, render_template
app=Flask(__name__)

@app.route("/")
def student():
    return render_template("student.html")

@app.route("/result", methods=["POST", "GET"])
def result():
    if request.method == "POST":
        return render_template("result.html", result=request.form)

if __name__ == "__main__":
    app.run(debug=True)