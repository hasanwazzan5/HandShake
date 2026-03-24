# Write SQLAlchemy class models here
from . import db
from datetime import datetime

class Users(db.Model):
    __tablename__ = "users"

    user_id = db.Column("user_id", db.Integer, primary_key = True) #PK
    name = db.Column(db.String(100))
    email = db.Column(db.String(50))
    avatar = db.Column(db.String(100))
    username = db.Column(db.String(20))

class Friends(db.Model):
    __tablename__ = "friends"

    Friends_id = db.Column("id", db.Integer, primary_key = True) #PK
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    friend_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

class Partnership(db.Model):
    __tablename__ = "partnership"

    Partnership_id = db.Column(db.Integer, primary_key = True)#PK
    partner_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))#FK
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))#FK
    partner_userhabit_id = db.Column(db.Integer, db.ForeignKey('user_habits.userhabit_id'))#FK
    user_userhabit_id = db.Column(db.Integer, db.ForeignKey('user_habits.userhabit_id'))#FK

class PartnershipRequest(db.Model):
    partnership_request_id = db.Column(db.Integer, primary_key=True)#PK
    sender_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))#FK
    user_userhabit_id = db.Column(db.Integer, db.ForeignKey('user_habits.userhabit_id'))#FK
    status = db.Column(db.String(20), default="pending")

class UserHabits(db.Model):
    __tablename__ = "user_habits"

    userhabit_id = db.Column(db.Integer, primary_key = True) #PK
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id')) #FK

    habit_name = db.Column(db.String)
    frequency = db.Column(db.String)
    goal = db.Column(db.String)

    dailyhabit = db.Column(db.Boolean)
    progress_number = db.Column(db.Integer)
    completed = db.Column(db.Boolean)
    completion_date = db.Column(db.String)
    streak = db.Column(db.Integer)

    def to_dict(self):
        return {
            "user":       self.userhabit_id,
            "habit_name": self.habit_name,
            "frequency":  self.frequency,
            "goal":       self.goal
        }


class HabitSubmissions(db.Model):
    __tablename__ = "habit_submissions"

    submission_id = db.Column(db.Integer, primary_key=True)
    userhabit_id = db.Column(db.Integer, db.ForeignKey('user_habits.userhabit_id'), nullable=False)
    image_path = db.Column(db.String(255), nullable=False, default="")
    image_blob = db.Column(db.LargeBinary)
    mime_type = db.Column(db.String(100), default="image/png")
    submission_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)