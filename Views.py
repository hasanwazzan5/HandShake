from flask import Blueprint, request, jsonify
from app.models import db, Habit, User

habits_bp = Blueprint('habits', __name__)

@habits_bp.route('/habits', methods=['POST'])
def add_habit():
    data = request.get_json()

    # Validate required fields
    if not data or 'habit_name' not in data or 'goal' not in data:
        return jsonify({"error": "habit_name and goal are required"}), 400

    new_habit = Habit(
        habit_name=data['habit_name'],
        goal=data['goal']
    )

    db.session.add(new_habit)
    db.session.commit()

    return jsonify({
        "message": "Habit added successfully",
        "habit": new_habit.to_dict()
    }), 201
nickname_bp = Blueprint('nickname', __name__)

@nickname_bp.route('/nickname', methods=['POST'])
def add_nickname():
    data = request.get_json()

    if not data or 'nickname' not in data:
        return jsonify({"error": "nickname is required"}), 400

    new_user = User(nickname=data['nickname'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "Nickname added successfully",
        "user": new_user.to_dict()
    }), 201
