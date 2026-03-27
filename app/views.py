# Flask views, for later
from datetime import datetime
from flask import render_template, url_for, Blueprint, redirect, session, request, jsonify, send_file
from . import db
from sqlalchemy import or_
from .models import UserHabits, Partnership, Users, PartnershipRequest, HabitSubmissions
from .authentication import Authenticator, authenticate
from collections import defaultdict
from io import BytesIO
from .partnership import Partner

site = Blueprint('site', __name__)


def _status_label(status):
    if not status:
        return "Pending review"
    status_map = {
        "pending": "Pending review",
        "approved": "Approved",
    }
    return status_map.get(status.lower(), status.capitalize())


def _is_partner_reviewer(owner_user_id, reviewer_user_id, owner_habit_id):
    low_id = min(owner_user_id, reviewer_user_id)
    high_id = max(owner_user_id, reviewer_user_id)

    partnership = Partnership.query.filter_by(partner_id=low_id, user_id=high_id).first()
    if not partnership:
        return False

    if owner_user_id == partnership.partner_id:
        return partnership.partner_userhabit_id == owner_habit_id
    return partnership.user_userhabit_id == owner_habit_id

@site.route('/')
def index():
    return render_template("index.html")

@site.route('/dashboard')
@authenticate
def dashboard():

    fullname = Authenticator.getFullname()
    current_user = Authenticator.getCurrentUser()

    user_habits = UserHabits.query.filter_by(user_id=current_user.user_id).all()
    partnerships = Partnership.query.filter(
        or_(
            Partnership.partner_id == current_user.user_id,
            Partnership.user_id == current_user.user_id
        )
    ).all()

    partner_name_by_habit_id = {}
    partner_habits = []
    partner_habit_ids = []
    for partnership in partnerships:
        if partnership.partner_id == current_user.user_id:
            own_habit_id = partnership.partner_userhabit_id
            partner_user_id = partnership.user_id
            partner_habit_id = partnership.user_userhabit_id
        else:
            own_habit_id = partnership.user_userhabit_id
            partner_user_id = partnership.partner_id
            partner_habit_id = partnership.partner_userhabit_id

        partner_user = Users.query.filter_by(user_id=partner_user_id).first()
        if partner_user and own_habit_id:
            partner_name_by_habit_id[own_habit_id] = partner_user.name

        partner_habit = UserHabits.query.filter_by(userhabit_id=partner_habit_id).first()
        if partner_user and partner_habit:
            partner_habit_ids.append(partner_habit.userhabit_id)
            partner_habits.append({
                "partner_name": partner_user.name or "Partner",
                "habit_name": partner_habit.habit_name or "Habit placeholder",
                "frequency": partner_habit.frequency.capitalize() if partner_habit.frequency else "Unknown",
                "streak": partner_habit.streak if partner_habit.streak is not None else 0,
                "partner_habit_id": partner_habit.userhabit_id
            })

    habits = []
    habit_ids = []
    for habit in user_habits:
        progress_number = habit.progress_number if habit.progress_number is not None else 0
        habit_ids.append(habit.userhabit_id)
        habits.append({
            "habit_id": habit.userhabit_id,
            "habit_name": habit.habit_name,
            "partner_name": partner_name_by_habit_id.get(habit.userhabit_id, "Not paired yet"),
            "streak": habit.streak if habit.streak is not None else 0,
            "progress": max(0, min(progress_number, 100))
        })

    submissions_grouped = defaultdict(list)
    if habit_ids:
        submissions = HabitSubmissions.query.filter(
            HabitSubmissions.userhabit_id.in_(habit_ids),
            HabitSubmissions.image_blob.isnot(None)
        ).order_by(HabitSubmissions.submission_date.desc()).all()

        for submission in submissions:
            submissions_grouped[submission.userhabit_id].append({
                "submission_date": submission.submission_date.strftime("%d/%m/%y"),
                "image_url": url_for('site.submission_image', submission_id=submission.submission_id),
                "status": _status_label(submission.status)
            })

    partner_submissions_grouped = defaultdict(list)
    if partner_habit_ids:
        partner_submissions = HabitSubmissions.query.filter(
            HabitSubmissions.userhabit_id.in_(partner_habit_ids),
            HabitSubmissions.image_blob.isnot(None)
        ).order_by(HabitSubmissions.submission_date.desc()).all()

        for submission in partner_submissions:
            partner_submissions_grouped[submission.userhabit_id].append({
                "submission_id": submission.submission_id,
                "submission_date": submission.submission_date.strftime("%d/%m/%y"),
                "image_url": url_for('site.submission_image', submission_id=submission.submission_id),
                "status": _status_label(submission.status)
            })

    habit_stats = {}
    habit_submissions = {}
    for habit in user_habits:
        submissions_for_habit = submissions_grouped.get(habit.userhabit_id, [])
        progress_number = habit.progress_number if habit.progress_number is not None else 0

        habit_submissions[str(habit.userhabit_id)] = submissions_for_habit
        habit_stats[str(habit.userhabit_id)] = {
            "habit_name": habit.habit_name,
            "current_streak": habit.streak if habit.streak is not None else 0,
            "longest_streak": habit.streak if habit.streak is not None else 0,
            "total_completions": len(submissions_for_habit),
            "completion_rate": f"{max(0, min(progress_number, 100))}%",
            "next_submission_due": "Placeholder due date"
        }

    pending_requests = PartnershipRequest.query.filter_by(
        sender_id=current_user.user_id,
        status="pending"
    ).all()

    pending_by_habit_id = {req.user_userhabit_id: req for req in pending_requests}
    pending_cards = []
    for habit in user_habits:
        if habit.userhabit_id in pending_by_habit_id:
            pending_cards.append({
                "habit_name": habit.habit_name,
                "status": "Pending"
            })

    return render_template(
        "site/dashboard.html",
        firstname=fullname.split()[0],
        habits=habits,
        partner_habits=partner_habits,
        pending_cards=pending_cards,
        habit_stats=habit_stats,
        habit_submissions=habit_submissions,
        partner_submissions=partner_submissions_grouped
    )

@site.route('/profile')
@authenticate
def profile():
    return render_template("site/profile.html")

@site.route('/login')
@authenticate
def login():
    return redirect(url_for('site.dashboard'))

@site.route('/logout')
def logout():
    return Authenticator.invalidateUser()

# The two routes here are temporary, just for testing the appearance of the html pages.
@site.route('/createhabit', methods=['GET', 'POST'])
@authenticate
def show_habit():
    if request.method == "POST":
        data = request.get_json()

        # Validate required fields
        if not data or 'habit_name' not in data or 'goal' not in data:
            return jsonify({"success": False, "error": "habit_name and goal are required"}), 400

        new_habit = UserHabits(
            user_id=Authenticator.getCurrentUser().user_id,
            habit_name=data['habit_name'],
            frequency=data['frequency'],
            goal=data['goal']
        )

        try:
            db.session.add(new_habit)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error adding habit: {e}")
            return jsonify({"success": False, "error": "An error occurred while adding the habit"}), 500
        

        senderUserhabitId = new_habit.userhabit_id
        noError = Partner.pairRequest(senderUserhabitId)
        if not noError:
            return jsonify({"success": False, "error": "A pending request already exists for this habit"}), 400

        # A safeguard
        print("Habit added successfully!")
        print(new_habit.to_dict())

        return jsonify({
            "success": True,
            "message": "Habit created and pairing request submitted",
            "redirect_url": url_for("site.dashboard")
        }), 201

    return render_template("site/createHabit.html")

@site.route('/pairingpage')
@authenticate
def show_pairing():
    current_user = Authenticator.getCurrentUser()
    own_habits = UserHabits.query.filter_by(user_id=current_user.user_id).all()
    default_habit_id = own_habits[0].userhabit_id if own_habits else None
    default_habit_name = own_habits[0].habit_name if own_habits else ""

    incoming_requests = Partner.GetPendingPairRequests()
    outgoing_requests = PartnershipRequest.query.filter_by(
        sender_id=current_user.user_id,
        status="pending"
    ).all()

    def to_card(request_obj, direction):
        sender_user = Users.query.filter_by(user_id=request_obj.sender_id).first()
        habit = UserHabits.query.filter_by(userhabit_id=request_obj.user_userhabit_id).first()

        if direction == "incoming":
            title = "Incoming pairing request"
            sender_label = sender_user.name if sender_user and sender_user.name else "Unknown user"
        else:
            title = "Your pending request"
            sender_label = "Waiting for a partner"

        return {
            "title": title,
            "sender_name": sender_label,
            "habit_name": habit.habit_name if habit and habit.habit_name else "Habit name placeholder",
            "goal": habit.goal if habit and habit.goal else "Goal placeholder",
            "frequency": habit.frequency.capitalize() if habit and habit.frequency else "Unknown",
            "status": request_obj.status.capitalize(),
            "request_id": request_obj.partnership_request_id
        }

    incoming_cards = [to_card(req, "incoming") for req in incoming_requests]
    outgoing_cards = [to_card(req, "outgoing") for req in outgoing_requests]

    return render_template(
        "site/pairingPage.html",
        incoming_cards=incoming_cards,
        outgoing_cards=outgoing_cards,
        default_habit_id=default_habit_id,
        default_habit_name=default_habit_name
    )

@site.route('/accept_pair_request', methods=["POST"])
@authenticate
def accept_partnership_request():
    if not request.is_json:
        return jsonify({"success": False, "error": "JSON body required"}), 400

    requestId = int(request.json["request_id"]) #use "request_id" in front end button
    newUserhabitId = int(request.json["new_userhabit_id"]) #use "new_userhabit_id" in front end button
    
    noError = Partner.pairAccept(requestId, newUserhabitId)
    if not noError:
        return jsonify({"success": False, "error": "Unable to accept pairing request"}), 403

    return jsonify({"success": True, "redirect_url": url_for("site.show_pairing")}), 200

@site.route("/remove_pairing", methods=["POST"])
@authenticate
def remove_partnership():
    partnerId = int(request.json["partner_id"]) #use "partner_id" in front end button
    Partner.unPair(partnerId)

    return redirect(url_for("show_pairing"))

@site.route('/camera')
@authenticate
def show_camera():
    return render_template("site/camera.html")

@site.route('/upload', methods=["POST"])
@authenticate
def upload_test():
    if request.method == "POST":
        if 'file' not in request.files:
            return jsonify({"success": False, "error": "No file part"}), 400

        habit_id = request.form.get("habit_id")
        if not habit_id:
            return jsonify({"success": False, "error": "habit_id is required"}), 400

        try:
            habit_id = int(habit_id)
        except ValueError:
            return jsonify({"success": False, "error": "habit_id must be an integer"}), 400

        current_user = Authenticator.getCurrentUser()
        habit = UserHabits.query.filter_by(
            userhabit_id=habit_id,
            user_id=current_user.user_id
        ).first()
        if not habit:
            return jsonify({"success": False, "error": "Habit not found for current user"}), 404

        file = request.files['file']
        if not file.filename:
            return jsonify({"success": False, "error": "Invalid file"}), 400

        blob_data = file.read()
        if not blob_data:
            return jsonify({"success": False, "error": "Image content is empty"}), 400

        mime_type = file.mimetype or "image/png"

        try:
            submission = HabitSubmissions(
                userhabit_id=habit_id,
                image_path="",
                image_blob=blob_data,
                mime_type=mime_type
            )
            db.session.add(submission)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"success": False, "error": f"Upload failed: {str(e)}"}), 500

        return jsonify({
            "success": True,
            "message": "File uploaded successfully",
            "submission_id": submission.submission_id,
            "habit_id": habit_id,
            "image_url": url_for('site.submission_image', submission_id=submission.submission_id)
        }), 201

    return render_template('site/navBar.html')


@site.route('/submission_image/<int:submission_id>')
@authenticate
def submission_image(submission_id):
    current_user = Authenticator.getCurrentUser()

    submission = HabitSubmissions.query.filter_by(submission_id=submission_id).first()
    if not submission or not submission.image_blob:
        return "Image not found", 404

    habit = UserHabits.query.filter_by(userhabit_id=submission.userhabit_id).first()
    if not habit:
        return "Image not found", 404

    can_view = habit.user_id == current_user.user_id or _is_partner_reviewer(
        owner_user_id=habit.user_id,
        reviewer_user_id=current_user.user_id,
        owner_habit_id=habit.userhabit_id
    )
    if not can_view:
        return "Forbidden", 403

    return send_file(
        BytesIO(submission.image_blob),
        mimetype=submission.mime_type or "image/png",
        as_attachment=False,
        download_name=f"submission_{submission.submission_id}.png"
    )


@site.route('/approve_submission', methods=["POST"])
@authenticate
def approve_submission():
    if not request.is_json:
        return jsonify({"success": False, "error": "JSON body required"}), 400

    submission_id = request.json.get("submission_id")
    if submission_id is None:
        return jsonify({"success": False, "error": "submission_id is required"}), 400

    try:
        submission_id = int(submission_id)
    except (TypeError, ValueError):
        return jsonify({"success": False, "error": "submission_id must be an integer"}), 400

    current_user = Authenticator.getCurrentUser()
    submission = HabitSubmissions.query.filter_by(submission_id=submission_id).first()
    if not submission:
        return jsonify({"success": False, "error": "Submission not found"}), 404

    habit = UserHabits.query.filter_by(userhabit_id=submission.userhabit_id).first()
    if not habit:
        return jsonify({"success": False, "error": "Habit not found"}), 404

    if habit.user_id == current_user.user_id:
        return jsonify({"success": False, "error": "You cannot approve your own submission"}), 403

    if not _is_partner_reviewer(
        owner_user_id=habit.user_id,
        reviewer_user_id=current_user.user_id,
        owner_habit_id=habit.userhabit_id
    ):
        return jsonify({"success": False, "error": "Not allowed to approve this submission"}), 403

    current_status = (submission.status or "pending").lower()
    if current_status == "approved":
        return jsonify({
            "success": True,
            "message": "Submission already approved",
            "status": "Approved",
            "updated_streak": habit.streak if habit.streak is not None else 0
        }), 200

    submission.status = "approved"
    submission.reviewed_by_user_id = current_user.user_id
    submission.reviewed_at = datetime.utcnow()
    habit.streak = (habit.streak or 0) + 1

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Submission approved",
        "status": "Approved",
        "updated_streak": habit.streak
    }), 200
