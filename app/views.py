# Flask views, for later
from flask import render_template, url_for, Blueprint
from . import db
from .models import Users

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