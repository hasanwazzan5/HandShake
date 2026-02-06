# Initialise Flask here
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "HandShake"

app.run(host="0.0.0.0",port="80")