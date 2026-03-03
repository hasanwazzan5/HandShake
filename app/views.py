# Flask views, for later
from flask import render_template, url_for, Blueprint, redirect, session, request
from . import db
from .models import Users
from .authentication import Authenticator
import os

site = Blueprint('site', __name__)

@site.route('/')
def index():
    return render_template("index.html")

@site.route('/dashboard')
def dashboard():
    result = Authenticator.validateUser()
    if result: return result

    fullname = Authenticator.getFullname()
    return render_template("site/dashboard.html", firstname=fullname.split()[0])

@site.route('/login')
def login():
    result = Authenticator.validateUser()
    if result: return result

    return redirect(url_for('site.dashboard'))

@site.route('/logout')
def logout():
    return Authenticator.invalidateUser()

# The two routes here are temporary, just for testing the appearance of the html pages.
@site.route('/createhabit')
def show_habit():
    result = Authenticator.validateUser()
    if result: return result

    return render_template("site/createHabit.html")

@site.route('/pairingpage')
def show_pairing():
    result = Authenticator.validateUser()
    if result: return result

    return render_template("site/pairingPage.html")

@site.route('/camera')
def show_camera():
    return render_template("site/camera.html")

@site.route('/upload', methods=["POST"])
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
    result = Authenticator.validateUser()
    if result: return result

    return render_template('site/navBar.html')
