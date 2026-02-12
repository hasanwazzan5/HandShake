# Write SQLAlchemy class models here
from . import db

# The issues with the 'users' is still here, please fix it

class users(db.model):
    user_id = db.Column("user_id", db.Integer, primary_key = True) #PK
    name = db.Column(db.String(100))
    email = db.Column(db.String(50))
    avatar = db.Column(db.String(100))
    username = db.Column(db.String(20))
    
class Friends(db.model):
    _id = db.Column("id", db.Integer, primary_key = True) #PK
    user_id = db.Column(db.Integer, db.ForeignKey('users'.id))
    friend_id = db.Column(db.Integer)

class Partnership(db.model):
    _id = db.Column("id", db.Integer, primary_key = True)#PK
    partner_id = db.Column("id", db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users'.id))

class Habits(db.model):
    habit_id = db.Column(db.Integer, primary_key = True)#PK
    habit_name = db.Column(db.String)
    goal = db.Column(db.String)  
    
class UserHabits(db.model):
    _id = db.Column("id", db.Integer, primary_key = True) #PK
    user_id = db.Column(db.Integer, db.ForeignKey('users'.id)) #FK
    habit_id = db.Column(db.Integer, db.ForeignKey('habits'.id)) #FK
    frequency = db.Column(db.Integer)
    progress_number = db.Column(db.Integer)
    completed = db.Column(db.Boolean)
    completion_date = db.Column(db.String)

