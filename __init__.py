from flask import Flask
from app.models import db
from app.views import habits_bp, nickname_bp

app = Flask(__name__)

# Database config (SQLite for now)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///handshake.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.register_blueprint(habits_bp) 
app.register_blueprint(nickname_bp)

# Create tables on first run
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return "HandShake"

app.run(host="0.0.0.0", port=80)

