# Flask views, for later
from flask import render_template, url_for, Blueprint, request
from .models import Users
import os

site = Blueprint('site', __name__)

@site.route('/')
def index():
    return render_template("index.html")

# The two routes here are temporary, just for testing the appearance of the html pages.
@site.route('/createhabit')
def show_habit():
    return render_template("site/createHabit.html")

@site.route('/pairingpage')
def show_pairing():
    return render_template("site/pairingPage.html")

@site.route('/navigationTest')
def show_navbar():
    return render_template('site/navBar.html')

@site.route('/login', methods=["GET", "POST"])
def login_test():
    if request.method == "POST":
        print(request.get_json())

        return "OK", 200
    
    return "Bad", 400

@site.route('/cameratest')
def show_camera():
    return render_template("site/camera.html")

@site.route('/uploadtest', methods=["POST"])
def upload_test():
    if request.method == "POST":
        if 'file' not in request.files:
            print("No file part")
            print(request.files)
            return "No file part", 400
        file = request.files['file']
        filename = file.filename

        file.save(os.path.join("app/static/uploads", filename))
    
        return "File uploaded successfully", 200