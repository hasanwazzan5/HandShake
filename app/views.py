# Flask views, for later
from flask import render_template, url_for, Blueprint, redirect, session, request
from . import db
from .models import UserHabits
from .authentication import Authenticator
import os
from .partnership import Partner

site = Blueprint('site', __name__)

@site.route('/')
def index():
    return render_template("index.html")

@site.route('/dashboard')
def dashboard():
    result = Authenticator.validateUser()
    if result: return result

    fullname = Authenticator.getFullname()
    
    return render_template("site/dashboard.html", firstname=fullname.split()[0])

@site.route('/login')
def login():
    result = Authenticator.validateUser()
    if result: return result

    return redirect(url_for('site.dashboard'))

@site.route('/logout')
def logout():
    return Authenticator.invalidateUser()

# The two routes here are temporary, just for testing the appearance of the html pages.
@site.route('/createhabit', methods=['GET', 'POST'])
def show_habit():
    result = Authenticator.validateUser()
    if result: return result


    if request.method == "POST":
        data = request.get_json()

        # Validate required fields
        if not data or 'habit_name' not in data or 'goal' not in data:
            return "error habit_name and goal are required", 400

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
            return "An error occurred while adding the habit", 500
        # A safeguard
        print("Habit added successfully!")
        print(new_habit.to_dict())

    return render_template("site/createHabit.html")

@site.route('/pairingpage')
def show_pairing():
    result = Authenticator.validateUser()
    if result: return result

    requests = Partner.GetPendingPairRequests()

    return render_template("site/pairingPage.html")#, requests=requests) #use this arg to connect to front end

@site.route('/send_pair_request', methods=["POST"])
def send_partnership_request():
    result = Authenticator.validateUser()
    if result: return result

    senderUserhabitId = int(request.form["sender_userhabit_id"]) #use "sender_userhabit_id" in front end form
    noError = Partner.pairRequest(senderUserhabitId)
    if not noError: return "Forbidden", 400

    return redirect(url_for("show_pairing"))

@site.route('/accept_pair_request', methods=["POST"])
def accept_partnership_request():
    result = Authenticator.validateUser()
    if result: return result

    requestId = int(request.form["request_id"]) #use "request_id" in front end form
    newUserhabitId = int(request.form["new_userhabit_id"]) #use "new_userhabit_id" in front end form
    
    noError = Partner.pairAccept(requestId, newUserhabitId)
    if not noError: return "Forbidden", 403

    return redirect(url_for("show_pairing"))

@site.route("/remove_pairing", methods=["POST"])
def remove_partnership():
    result = Authenticator.validateUser()
    if result: return result

    partnerId = int(request.form["partner_id"]) #use "partner_id" in front end form
    Partner.unPair(partnerId)

    return redirect(url_for("show_pairing"))

@site.route('/camera')
def show_camera():
    result = Authenticator.validateUser()
    if result: return result

    return render_template("site/camera.html")

@site.route('/upload', methods=["POST"])
def upload_test():
    result = Authenticator.validateUser()
    if result: return result

    if request.method == "POST":
        if 'file' not in request.files:
            print("No file part")
            print(request.files)
            return "No file part", 400
        file = request.files['file']
        filename = file.filename

        file.save(os.path.join("app/static/uploads", filename))
    
        return "File uploaded successfully", 200

    return render_template('site/navBar.html')
