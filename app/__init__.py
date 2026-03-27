# Initialise Flask here
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import secrets

db = SQLAlchemy()
DB_NAME = "main.db"


def ensure_submission_blob_columns():
    columns = db.session.execute(text("PRAGMA table_info(habit_submissions)")).mappings().all()
    if not columns:
        return

    column_names = {column["name"] for column in columns}

    if "image_blob" not in column_names:
        db.session.execute(text("ALTER TABLE habit_submissions ADD COLUMN image_blob BLOB"))

    if "mime_type" not in column_names:
        db.session.execute(text("ALTER TABLE habit_submissions ADD COLUMN mime_type TEXT DEFAULT 'image/png'"))

    if "status" not in column_names:
        db.session.execute(text("ALTER TABLE habit_submissions ADD COLUMN status TEXT DEFAULT 'pending'"))

    if "reviewed_by_user_id" not in column_names:
        db.session.execute(text("ALTER TABLE habit_submissions ADD COLUMN reviewed_by_user_id INTEGER"))

    if "reviewed_at" not in column_names:
        db.session.execute(text("ALTER TABLE habit_submissions ADD COLUMN reviewed_at DATETIME"))

    db.session.commit()

def createApp():
    app = Flask(__name__)
    app.secret_key = secrets.token_hex(32)

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False
    db.init_app(app)
    
    from .views import site
    app.register_blueprint(site)

    print("Registered routes:")  # Add this
    print(app.url_map)  # Add this

    with app.app_context():
        db.create_all()
        ensure_submission_blob_columns()

    return app