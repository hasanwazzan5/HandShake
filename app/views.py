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
    if result:
        return result
    return redirect(url_for('site.loggedin'))

@site.route('/loggedin')
def loggedin():
    result = Authenticator.validateUser()
    if result:
        return result
    
    return f"""
        YOU HAVE LOGGED IN <br>
        Login time: {Authenticator.getTimeAuthenticated(formatted=True)} <br>
        Username: {Authenticator.getUsername()} <br>
        Fullname: {Authenticator.getFullname()} <br>
        """

@site.route('/logout')
def logout():
    return Authenticator.invalidateUser()

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