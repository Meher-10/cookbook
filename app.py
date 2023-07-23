from flask import Flask,Blueprint,render_template, request, redirect, url_for, session, flash, jsonify, make_response
from users.routes import routes_bp

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Add a secret key for session encryption
app.register_blueprint(routes_bp, url_prefix='/')

@app.route('/')
def home():
    return render_template("base.html")

@app.route('/signIn')
def signup():
    return render_template("signIn.html")

if __name__ == '__main__':
    app.run(debug=True)
