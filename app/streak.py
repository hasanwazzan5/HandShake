from . import db
from .__init__ import app
from .models import Users, UserHabits
import schedule
from schedule import every, repeat
from datetime import time, timedelta, datetime
from flask import session

user_id = session.get('user_id')
user  = Users.query.get(user_id)

@app.route('\update-streak\<int:habit_id',methods = ['POST']) #when habit complete 
def update_streak(habit_id):
    habit = UserHabits.query.get(habit_id)
    if habit.completed == True:
        habit.streak = habit.streak + 1
    db.session.commit()

@repeat(every(1).day.at("01:00")) #every day at 1 am function runs
def refresh_daily_habits(habit_id):
    for habit in UserHabits:
        if habit.daily and habit.completed == False: # if a daily habit and not complete reset streak
            habit.streak = 0 
    db.session.commit()