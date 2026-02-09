# Initialise Flask here
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False

db = SQLAlchemy(app)

if __name__ == "__main__":
    
    app.run(debug=True)
app.app_context()


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

app.run(host="0.0.0.0",port="80",debug=True)