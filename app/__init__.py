# Initialise Flask here
from flask import Flask, render_template, url_for

app = Flask(__name__)

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

app.run(host="0.0.0.0",port="80",debug=True)