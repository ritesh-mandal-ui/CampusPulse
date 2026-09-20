from flask import Blueprint

from models.student import Student
from models.company import Company
from models.job import Job
from models.application import Application
from models.offer import Offer


public_bp = Blueprint(
    "public",
    __name__,
    url_prefix="/api/public"
)


@public_bp.route("/summary", methods=["GET"])
def get_public_summary():
    total_students = Student.query.count()
    total_companies = Company.query.count()
    total_jobs = Job.query.count()
    total_applications = Application.query.count()
    total_offers = Offer.query.count()

    return {
        "total_students": total_students,
        "total_companies": total_companies,
        "total_jobs": total_jobs,
        "total_applications": total_applications,
        "total_offers": total_offers
    }