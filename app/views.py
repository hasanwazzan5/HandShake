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

@site.route('/login')
def login():
    result = Authenticator.validateUser()
    if result: return result

    return redirect(url_for('site.loggedin'))

@site.route('/loggedin')
def loggedin():
    '''
    Page that user is sent to after logging in
    The content of this page is temporary
    '''

    result = Authenticator.validateUser()
    if result: return result

    me = Users.query.filter_by(username=session["username"]).first()
    
    return f"""
        YOU HAVE LOGGED IN! <br>
        <br>
        Login time: {Authenticator.getTimeAuthenticated(formatted=True)} <br>
        <br>
        UserID: {me.user_id} <br>
        Fullname: {me.name} <br>
        Avatar: {me.avatar} <br>
        Avatar: {me.email} <br>
        Username: {me.username} <br>
        """

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
    result = Authenticator.validateUser()
    if result: return result

    return render_template('site/navBar.html')
