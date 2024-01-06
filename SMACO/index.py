from flask import Blueprint, render_template

index = Blueprint(__name__,"index")

@index.route("/")

def home():
    return render_template("index.html", routing="/calculator/")