from app import db, createApp
from app.models import Users, UserHabits, Habits
app = createApp()

with app.app_context():
    user  = Users(name = "john", email = "john@email.com", username = "johnjon11" )
    db.session.add(user)
    db.session.commit()

    habit = Habits(habit_name = "running", goal = "becoming a runner")
    habit2 = Habits(habit_name = "gym", goal = "become a strong person")
    db.session.add(habit)
    db.session.add(habit2)
    db.session.commit()

    userhabit = UserHabits(user_id = 1, habit_id = 1, frequency = 7, dailyhabit = True, progress_number = 5, completed = False, streak = 5) 
    userhabit2 = UserHabits( user_id = 2, habit_id = 2 ,frequency = 5, dailyhabit = False, progress_number = 7, completed = True, streak = 7 )
    db.session.add(userhabit)
    db.session.add(userhabit2)
    db.session.commit()
    print("Seeded! Habits:", UserHabits.query.all())