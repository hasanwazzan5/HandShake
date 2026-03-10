from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Habit(db.Model):
    __tablename__ = 'habits'

    habit_id   = db.Column(db.Integer, primary_key=True, autoincrement=True)
    habit_name = db.Column(db.String(100), nullable=False)
    goal       = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            "habit_id":   self.habit_id,
            "habit_name": self.habit_name,
            "goal":       self.goal
        }

