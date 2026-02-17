# Initialise Flask here
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = "main.db"

def createApp():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False
    db.init_app(app)
    
    from .views import site
    app.register_blueprint(site)

    print("Registered routes:")  # Add this
    print(app.url_map)  # Add this

    with app.app_context():
        db.create_all()

    return app