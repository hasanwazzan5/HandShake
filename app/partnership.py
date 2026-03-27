# functions to manage partnerships in the database
from . import db
from .models import Partnership, PartnershipRequest
from .authentication import Authenticator


class Partner:
    @staticmethod
    def pairRequest(userHabitId):
        currentUser = Authenticator.getCurrentUser()

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
        currentUser = Authenticator.getCurrentUser()

        req = PartnershipRequest.query.filter_by(partnership_request_id=requestId).first()
        if not req or req.status != "pending":
            return False

        partnerId = req.sender_id

        low = min((partnerId, req.user_userhabit_id), (currentUser.user_id, newUserHabitId))
        high = max((partnerId, req.user_userhabit_id), (currentUser.user_id, newUserHabitId))

        if not Partner.arePartnered(low[0], high[0]):
            newPartnership = Partnership(
                partner_id=low[0],
                user_id=high[0],
                partner_userhabit_id=low[1],
                user_userhabit_id=high[1]
            )
            db.session.add(newPartnership)
            req.status = "accepted"

            related_pending_requests = PartnershipRequest.query.filter(
                PartnershipRequest.status == "pending",
                PartnershipRequest.partnership_request_id != req.partnership_request_id,
                PartnershipRequest.user_userhabit_id.in_([
                    req.user_userhabit_id,
                    newUserHabitId
                ])
            ).all()
            for pending_req in related_pending_requests:
                pending_req.status = "paired"

            db.session.commit()
        else:
            return False

        return True

    @staticmethod
    def GetPendingPairRequests():
        currentUser = Authenticator.getCurrentUser()

        requests = PartnershipRequest.query.filter(
            PartnershipRequest.status == "pending",
            PartnershipRequest.sender_id != currentUser.user_id
        ).all()

        return requests

    @staticmethod
    def unPair(partnerId):
        currentUser = Authenticator.getCurrentUser()

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
