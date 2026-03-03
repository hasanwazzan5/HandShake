# functions to manage partnerships in the database
from flask import session
from . import db
from .models import Partnership, Users

class Partner:
    @staticmethod
    def pair(partnerUsername):
        partnerUser = Users.query.filter_by(username=partnerUsername).first()
        currentUser = Users.query.filter_by(username=session["username"]).first()

        if partnerUser and not Partner.arePartnered(currentUser.user_id, partnerUser.user_id):
            newPartnership = Partnership(partner_id=partnerUser.user_id, user_id=currentUser.user_id)
            db.session.add(newPartnership)
            db.session.commit()

    @staticmethod
    def unPair(partnerUsername):
        partnerUser = Users.query.filter_by(username=partnerUsername).first()
        currentUser = Users.query.filter_by(username=session["username"]).first()

        if partnerUser and Partner.arePartnered(currentUser.user_id, partnerUser.user_id):
            partnership = Partnership.query.filter_by(partner_id=partnerUser.user_id, user_id=currentUser.user_id).first()
            db.session.delete(partnership)
            db.session.commit()

    @staticmethod
    def arePartnered(currentUserId, partnerUserId):
        partnership = Partnership.query.filter_by(partner_id=currentUserId, user_id=partnerUserId).first()
        
        if partnership:
            return True
        else:
            return False