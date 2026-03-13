# functions to manage partnerships in the database
from flask import session
from . import db
from .models import Partnership, Users, PartnershipRequest

class Partner:
    @staticmethod
    def pairRequest(userHabitId):
        currentUser = Users.query.filter_by(username=session["username"]).first()

        existing = PartnershipRequest.query.filter_by(
            sender_id=currentUser.user_id,
            user_userhabit_id=userHabitId,
        ).first()
        
        if existing:
            return False

        req = PartnershipRequest(
            sender_id=currentUser.user_id,
            user_userhabit_id=userHabitId,
            status="pending"
        )
        
        db.session.add(req)
        db.session.commit()

        return True

    @staticmethod
    def pairAccept(requestId, newUserHabitId):
        currentUser = Users.query.filter_by(username=session["username"]).first()

        req = PartnershipRequest.query.filter_by(partnership_request_id=requestId).first()

        if req.status != "pending":
            return False
       
       #creating partnership
        partnerId = req.sender_id

        low = min((partnerId, req.user_userhabit_id), (currentUser.user_id, newUserHabitId))
        high = max((partnerId, req.user_userhabit_id), (currentUser.user_id, newUserHabitId))

        if not Partner.arePartnered(low, high):
            newPartnership = Partnership(
                partner_id=low[0],
                user_id=high[1],
                partner_userhabit_id=low[0],
                user_userhabit_id=high[1]
            )
            db.session.add(newPartnership)
            req.status = "accepted" 
            db.session.commit()
        else:
            return False
        
        return True

    @staticmethod
    def GetPendingPairRequests():
        currentUser = Users.query.filter_by(username=session["username"]).first()

        requests = PartnershipRequest.query.filter(
            PartnershipRequest.status == "pending",
            PartnershipRequest.sender_id != currentUser.user_id
        ).all()

        return requests

    @staticmethod
    def unPair(partnerId):
        currentUser = Users.query.filter_by(username=session["username"]).first()

        low = min(partnerId, currentUser.user_id)
        high = max(partnerId, currentUser.user_id)

        if Partner.arePartnered(low, high):
            partnership = Partnership.query.filter_by(partner_id=low, user_id=high).first()
            db.session.delete(partnership)
            db.session.commit()

    @staticmethod
    def arePartnered(low_id, high_id):
        partnership = Partnership.query.filter_by(partner_id=low_id, user_id=high_id).first()
        
        if partnership:
            return True
        else:
            return False