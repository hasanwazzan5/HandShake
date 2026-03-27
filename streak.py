from datetime import datetime, timedelta
import time

import schedule
from schedule import every, repeat

from app import createApp, db
from app.models import HabitSubmissions, UserHabits


app = createApp()


def _cadence_days(habit):
    frequency = (habit.frequency or "").strip().lower()
    return 7 if frequency == "weekly" else 1


def _parse_completion_date(completion_date_value):
    if not completion_date_value:
        return None
    try:
        return datetime.fromisoformat(completion_date_value).date()
    except ValueError:
        return None


def _latest_upload_date(habit_id):
    latest_submission = HabitSubmissions.query.filter_by(userhabit_id=habit_id).filter(
        HabitSubmissions.image_blob.isnot(None)
    ).order_by(HabitSubmissions.submission_date.desc()).first()

    if latest_submission and latest_submission.submission_date:
        return latest_submission.submission_date.date()
    return None


@repeat(every(1).day.at("01:00"))
def reset_missed_streaks():
    today = datetime.utcnow().date()
    habits = UserHabits.query.all()
    did_change = False

    for habit in habits:
        cadence_days = _cadence_days(habit)
        last_upload_date = _latest_upload_date(habit.userhabit_id)
        last_completed_date = _parse_completion_date(habit.completion_date)
        last_activity_date = last_upload_date or last_completed_date

        if not last_activity_date:
            if (habit.streak or 0) > 0:
                habit.streak = 0
                habit.completed = False
                did_change = True
            continue

        due_date = last_activity_date + timedelta(days=cadence_days)
        if today > due_date and (habit.streak or 0) > 0:
            habit.streak = 0
            habit.completed = False
            did_change = True

    if did_change:
        db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        while True:
            schedule.run_pending()
            time.sleep(1)


