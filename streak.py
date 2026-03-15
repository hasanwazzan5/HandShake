from app import db,createApp
from app.models import Users, UserHabits
import schedule
from schedule import every, repeat
from datetime import time, timedelta, datetime
from flask import session
import time
app = createApp()


@app.route('/completedhabit') #should run whenever habit completes
def increment_streak():#when habit complete, streak increases
    habits = db.session.query(UserHabits).filter_by(completed = True).all()
    for habit in habits:
        habit.streak = habit.streak + 1
    db.session.commit()


@repeat(every(1).day.at("01:00")) #every day at 1 am function runs
def refresh_daily_habits():
    habits = db.session.query(UserHabits).filter_by(completed = False).all()#queries all habits where completed is False
    for habit in habits:
        habit.streak = 0
    db.session.commit()

with app.app_context():
    # refresh_daily_habits()
    # increment_streak()

    while True:
        schedule.run_pending()
        time.sleep(1)


