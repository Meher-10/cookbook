from flask import Flask,Blueprint,render_template, request, redirect, url_for, session, flash, jsonify, make_response
from users.routes import routes_bp

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Add a secret key for session encryption
app.register_blueprint(routes_bp, url_prefix='/')

@app.route('/')
def home():
    return render_template("base.html")
@app.route('/userregister')
def userregister():
    return render_template("register.html")

@app.route('/logIn')
def signin():
    return render_template("logIn.html")
@app.route('/addvideos')
def addvideos():
    return render_template("addrecipe.html")
@app.route('/displayvideos')
def displayvideos():
    return render_template("displayy3.html")
@app.route('/myrecipe')
def displaymyrecipe():
    return render_template("display.html")
@app.route('/about')
def about():
    return render_template("about.html")


if __name__ == '__main__':
    app.run(debug=True)
