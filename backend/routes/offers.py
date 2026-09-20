from datetime import date, datetime

from flask import Blueprint, request

from extensions import db
from models.application import Application
from models.offer import Offer
from utils.decorators import token_required


offers_bp = Blueprint(
    "offers",
    __name__,
    url_prefix="/api/offers"
)


@offers_bp.route("", methods=["GET"])
@token_required
def get_offers(payload):
    if payload["role"] == "STUDENT":
        from models.student import Student

        student = Student.query.filter_by(
            user_id=payload["user_id"]
        ).first()

        if not student:
            return {"error": "Student profile not found"}, 404

        applications = Application.query.filter_by(
            student_id=student.student_id
        ).all()

        application_ids = [
            application.application_id
            for application in applications
        ]

        offers = Offer.query.filter(
            Offer.application_id.in_(application_ids)
        ).order_by(Offer.offer_id).all()

    elif payload["role"] in ["TPO", "ADMIN", "SUPER_ADMIN"]:
        offers = Offer.query.order_by(Offer.offer_id).all()

    else:
        return {"error": "Access denied"}, 403

    return {
        "offers": [
            {
                "offer_id": offer.offer_id,
                "application_id": offer.application_id,
                "salary_lpa": float(offer.salary_lpa),
                "offer_date": offer.offer_date.isoformat(),
                "offer_status": offer.offer_status
            }
            for offer in offers
        ]
    }


@offers_bp.route("", methods=["POST"])
@token_required
def create_offer(payload):
    if payload["role"] not in ["TPO", "ADMIN", "SUPER_ADMIN"]:
        return {"error": "Only TPO or admin can create offers"}, 403

    data = request.get_json(silent=True)

    if not data:
        return {"error": "Request body is required"}, 400

    application_id = data.get("application_id")
    salary_lpa = data.get("salary_lpa")
    offer_status = data.get("offer_status", "ACTIVE")

    if not application_id or salary_lpa is None:
        return {
            "error": "application_id and salary_lpa are required"
        }, 400

    if offer_status not in ["ACTIVE", "ACCEPTED", "DECLINED"]:
        return {
            "error": "Invalid offer status"
        }, 400

    application = Application.query.get(application_id)

    if not application:
        return {"error": "Application not found"}, 404

    if application.status != "SELECTED":
        return {
            "error": "Offer can only be created for a selected application"
        }, 400

    existing_offer = Offer.query.filter_by(
        application_id=application_id
    ).first()

    if existing_offer:
        return {"error": "Offer already exists"}, 409

    offer_date_value = data.get("offer_date")

    if offer_date_value:
        try:
            offer_date = datetime.strptime(
                offer_date_value,
                "%Y-%m-%d"
            ).date()
        except (TypeError, ValueError):
            return {
                "error": "offer_date must be in YYYY-MM-DD format"
            }, 400
    else:
        offer_date = date.today()

    offer = Offer(
        application_id=application_id,
        salary_lpa=salary_lpa,
        offer_date=offer_date,
        offer_status=offer_status
    )

    db.session.add(offer)
    db.session.commit()

    return {
        "message": "Offer created successfully",
        "offer_id": offer.offer_id,
        "application_id": offer.application_id,
        "salary_lpa": float(offer.salary_lpa),
        "offer_date": offer.offer_date.isoformat(),
        "offer_status": offer.offer_status
    }, 201