# Write SQLAlchemy class models here
from . import db

# The issues with the 'users' is still here, and db.model should be db.Model.
# Run main.py to see syntax errors

class users(db.Model):
    __tablename__ = "users"

    user_id = db.Column("user_id", db.Integer, primary_key = True) #PK
    name = db.Column(db.String(100))
    email = db.Column(db.String(50))
    avatar = db.Column(db.String(100))
    username = db.Column(db.String(20))
    
class Friends(db.Model):
    __tablename__ = "friends"

    Friends_id = db.Column("id", db.Integer, primary_key = True) #PK
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    friend_id = db.Column(db.Integer)

class Partnership(db.Model):
    __tablename__ = "partnership"

    Partnership_id = db.Column("id", db.Integer, primary_key = True)#PK
    partner_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

class Habits(db.Model):
    __tablename__ = "habits"

    habit_id = db.Column("habit_id",db.Integer, primary_key = True)#PK
    habit_name = db.Column(db.String)
    goal = db.Column(db.String)  
    
class UserHabits(db.Model):
    __tablename__ = "user_habits"

    userhabit_id = db.Column("id", db.Integer, primary_key = True) #PK
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id')) #FK
    habit_id = db.Column(db.Integer, db.ForeignKey('habits.habit_id')) #FK
    frequency = db.Column(db.Integer)
    progress_number = db.Column(db.Integer)
    completed = db.Column(db.Boolean)
    completion_date = db.Column(db.String)

