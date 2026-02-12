# Flask views, for later
from flask import render_template, url_for
from . import db
from .models import users
from main import app


@app.route('/')
def index():
    return render_template("index.html")

# The two routes here are temporary, just for testing the appearance of the html pages.
@app.route('/createhabit')
def show_habit():
    return render_template("site/createHabit.html")

@app.route('/pairingpage')
def show_pairing():
    return render_template("site/pairingPage.html")

@app.route('/navigationTest')
def show_navbar():
    return render_template('site/navBar.html')

@app.route('/testdb')
def upload_data():
    sample_data = users("19", "john", "john@john.mail", "sample", "johndoe12333")
    db.session.add(sample_data)