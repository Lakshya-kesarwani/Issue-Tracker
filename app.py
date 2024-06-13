from flask import Flask,render_template,jsonify,Request
from sqlalchemy import text
app=Flask(__name__)

@app.route("/")
def home_page():
    return render_template("home-page.html")