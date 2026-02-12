# Write SQLAlchemy class models here
# Write SQLAlchemy class models here
from . import db

class users(db.Model):
    user_id = db.Column("user_id", db.Integer, primary_key = True) #PK
    name = db.Column(db.String(100))
    email = db.Column(db.String(50))
    avatar = db.Column(db.String(100))
    username = db.Column(db.String(20))
    
class Friends(db.Model):
    link2_id = db.Column("id", db.Integer, primary_key = True) #PK
    user_id = db.Column(db.Integer, db.ForeignKey(users.user_id))
    friend_id = db.Column(db.Integer)

class Partnership(db.Model):
    link_id = db.Column("id", db.Integer, primary_key = True)#PK
    partner_id = db.Column("id", db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey(users.user_id))

class Habits(db.Model):
    habit_id = db.Column(db.Integer, primary_key = True)#PK
    habit_name = db.Column(db.String)
    goal = db.Column(db.String)

class UserHabits(db.Model):
    _id = db.Column("id", db.Integer, primary_key = True) #PK
    user_id = db.Column(db.Integer, db.ForeignKey(users.user_id)) #FK
    habit_id = db.Column(db.Integer, db.ForeignKey(Habits.habit_id)) #FK
    frequency = db.Column(db.Integer)
    progress_number = db.Column(db.Integer)
    completed = db.Column(db.Boolean)
    completion_date = db.Column(db.String)
