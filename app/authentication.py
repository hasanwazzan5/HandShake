import secrets
import string
import datetime

#import requests #not required in the current version (if used, add to requirments.txt)
from urllib.parse import quote
from markupsafe import escape
from flask import session, request, redirect, make_response

from .models import Users
from . import db

UOM_AUTH_URL = "http://studentnet.cs.manchester.ac.uk/authenticate/"
UOM_AUTH_LOGOUT_URL = "http://studentnet.cs.manchester.ac.uk/systemlogout.php"
LOGGEDIN_URL = "http://127.0.0.1:5000/dashboard"


class Register:
    @staticmethod
    def registerUser():
        newUser = Users(username=session["username"], name=session["fullname"])
        db.session.add(newUser)
        db.session.commit()

    @staticmethod
    def isRegistered():
        if Users.query.filter_by(username=session["username"]).first():
            return True
        else:
            return False

class Authenticator:

    @staticmethod
    def validateUser():
        if Authenticator.isAuthenticated():
            return
        
        elif not request.args.get("csticket") or  not session.get("csticket"):
            return Authenticator.sendForAuthentication()

        elif request.args.get("csticket") != session.get("csticket"):
            return Authenticator.sendForAuthentication()

        Authenticator.recordAuthenticatedUser()
        return

        #Fully safe version needs to include the following lines
        #but they currently don't work
        '''
        elif Authenticator.isGETParametersMatchingServerAuthentication():
            Authenticator.recordAuthenticatedUser()
            return
        
        else:
            return Authenticator.failAuthentication()
        '''

    @staticmethod
    def isAuthenticated():
        authenticatedTimestamp = Authenticator.getTimeAuthenticated()
        if authenticatedTimestamp and (type(authenticatedTimestamp) == float):
            return True
        else:
            return False
    
    @staticmethod
    def sendForAuthentication():
        csticket = Authenticator.generateCSTicket()
        session["csticket"] = csticket
        url = Authenticator.getAuthenticationURL("validate")
        return redirect(url)

    @staticmethod
    def isGETParametersMatchingServerAuthentication():
        url = Authenticator.getAuthenticationURL("confirm")
        url += ("&username=" + quote(escape(request.args.get("username"))) +
                "&fullname=" + quote(escape(request.args.get("fullname"))))
            
        if Authenticator.fileGetContent(url) != "true":
            return False
        else:
            return True

    @staticmethod
    def failAuthentication():
        errormessage = """
        <h1>ERROR</h1>
        <p>Authentication failed.</p>
        <p>Suspected man-in-the-middle attack.</p>
        <p>The data in the URL GET parameters do not match those authenticated on the CAS proxy server.</p>
        """
        return make_response(errormessage, 403)  # 403 Forbidden

    @staticmethod
    def recordAuthenticatedUser():
        currentDatetime = datetime.datetime.now()
        unixTime = currentDatetime.timestamp()

        session["authenticated"] = unixTime
        session["username"] = escape(request.args.get("username"))
        session["fullname"] = escape(request.args.get("fullname"))

        if not Register.isRegistered():
            Register.registerUser()

    '''
    @staticmethod
    def fileGetContent(url):
        try:
            response = requests.get(url, timeout=5)
            return response.text.strip()

        except requests.RequestException:
            return "false"
    '''
        
    @staticmethod
    def generateCSTicket(length=16):
        """Generates a random string of specified length to be used as a csticket."""
        chars = string.ascii_letters + string.digits
        return ''.join(secrets.choice(chars) for _ in range(length))
        


    @staticmethod
    def getAuthenticationURL(command):
        csticket = session["csticket"]
        url = f"{UOM_AUTH_URL}?url={LOGGEDIN_URL}&csticket={csticket}&version=3&command={command}"
        return url

    @staticmethod
    def getTimeAuthenticated(formatted=False):
        timestamp = session.get("authenticated")
        if formatted:
            return datetime.datetime.fromtimestamp(timestamp)
        return timestamp
    
    @staticmethod
    def getUsername():
        return session.get("username")
    
    @staticmethod
    def getFullname():
        return session.get("fullname")
    
    @staticmethod
    def invalidateUser():
        session.clear()
        return redirect(UOM_AUTH_LOGOUT_URL)