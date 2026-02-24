# Flask views, for later
from flask import render_template, url_for, Blueprint, redirect, session
from . import db
from .models import Users
from .authentication import Authenticator

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
    result = Authenticator.validateUser()
    if result: return result

    return render_template('site/navBar.html')