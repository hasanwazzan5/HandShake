# functions to manage partnerships in the database
from flask import session
from . import db
from .models import Partnership, Users, PartnershipRequest

class Partner:
    @staticmethod
    def pairRequest(receiverId):
        currentUser = Users.query.filter_by(username=session["username"]).first()

        low = min(receiverId, currentUser.user_id)
        high = max(receiverId, currentUser.user_id)
        if Partner.arePartnered(low, high):
            return False

        if receiverId == currentUser.user_id:
            return False

        existing = PartnershipRequest.query.filter_by(
            sender_id=currentUser.user_id,
            receiver_id=receiverId,
            status="pending"
        ).first()
        
        if existing:
            return False

        req = PartnershipRequest(sender_id=currentUser.user_id, receiver_id=receiverId)
        db.session.add(req)
        db.session.commit()

        return True

    @staticmethod
    def pairAccept(requestId):
        currentUser = Users.query.filter_by(username=session["username"]).first()

        req = PartnershipRequest.query.filter_by(partnership_request_id=requestId).first()

        if req.receiver_id != currentUser.user_id:
            return False

        req.status = "accepted"
        db.session.commit()
        
        Partner.pair(req.sender_id)

        return True


    @staticmethod
    def pairReject(requestId):
        currentUser = Users.query.filter_by(username=session["username"]).first()

        req = PartnershipRequest.query.filter_by(partnership_request_id=requestId).first()

        if req.receiver_id != currentUser.user_id:
            return False

        req.status = "rejected"
        db.session.commit()

        return True

    @staticmethod
    def GetPendingPairRequests():
        currentUser = Users.query.filter_by(username=session["username"]).first()

        requests = PartnershipRequest.query.filter_by(
            receiver_id=currentUser.user_id,
            status="pending"
        ).all()

        return requests 

    @staticmethod
    def pair(partnerId):
        currentUser = Users.query.filter_by(username=session["username"]).first()

        low = min(partnerId, currentUser.user_id)
        high = max(partnerId, currentUser.user_id)

        if not Partner.arePartnered(low, high):
            newPartnership = Partnership(partner_id=low, user_id=high)
            db.session.add(newPartnership)
            db.session.commit()

    @staticmethod
    def unPair(partnerId):
        currentUser = Users.query.filter_by(username=session["username"]).first()

        low = min(partnerId, currentUser.user_id)
        high = max(partnerId, currentUser.user_id)

        if not Partner.arePartnered(low, high):
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