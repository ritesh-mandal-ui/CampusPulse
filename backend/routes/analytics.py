from flask import Blueprint

from extensions import db
from models.student import Student
from models.company import Company
from models.job import Job
from models.application import Application
from models.offer import Offer
from utils.decorators import token_required


analytics_bp = Blueprint(
    "analytics",
    __name__,
    url_prefix="/api/analytics"
)


@analytics_bp.route("/summary", methods=["GET"])
@token_required
def get_summary(payload):
    if payload["role"] not in [
        "TPO",
        "ADMIN",
        "SUPER_ADMIN"
    ]:
        return {"error": "Access denied"}, 403

    total_students = Student.query.count()
    total_companies = Company.query.count()
    total_jobs = Job.query.count()
    total_applications = Application.query.count()

    selected_applications = Application.query.filter_by(
        status="SELECTED"
    ).all()

    selected_student_ids = {
        application.student_id
        for application in selected_applications
    }

    selected_students = len(selected_student_ids)

    total_offers = Offer.query.count()

    placement_rate = (
        (selected_students / total_students) * 100
        if total_students > 0
        else 0
    )

    average_package = db.session.query(
        db.func.avg(Offer.salary_lpa)
    ).scalar()

    highest_package = db.session.query(
        db.func.max(Offer.salary_lpa)
    ).scalar()

    return {
        "total_students": total_students,
        "total_companies": total_companies,
        "total_jobs": total_jobs,
        "total_applications": total_applications,
        "selected_students": selected_students,
        "total_offers": total_offers,
        "placement_rate": round(placement_rate, 2),
        "average_package": (
            float(average_package)
            if average_package is not None
            else 0
        ),
        "highest_package": (
            float(highest_package)
            if highest_package is not None
            else 0
        )
    }


@analytics_bp.route("/application-status", methods=["GET"])
@token_required
def get_application_status(payload):
    if payload["role"] not in [
        "TPO",
        "ADMIN",
        "SUPER_ADMIN"
    ]:
        return {"error": "Access denied"}, 403

    statuses = [
        "APPLIED",
        "SHORTLISTED",
        "INTERVIEW",
        "SELECTED",
        "REJECTED",
        "WITHDRAWN"
    ]

    result = []

    for status in statuses:
        count = Application.query.filter_by(
            status=status
        ).count()

        result.append({
            "status": status,
            "count": count
        })

    return {
        "application_status": result
    }


@analytics_bp.route("/company-placements", methods=["GET"])
@token_required
def get_company_placements(payload):
    if payload["role"] not in [
        "TPO",
        "ADMIN",
        "SUPER_ADMIN"
    ]:
        return {"error": "Access denied"}, 403

    companies = Company.query.order_by(
        Company.company_id
    ).all()

    result = []

    for company in companies:
        job_ids = [
            job.job_id
            for job in Job.query.filter_by(
                company_id=company.company_id
            ).all()
        ]

        if not job_ids:
            selected_count = 0
        else:
            selected_student_ids = {
                application.student_id
                for application in Application.query.filter(
                    Application.job_id.in_(job_ids),
                    Application.status == "SELECTED"
                ).all()
            }

            selected_count = len(selected_student_ids)

        result.append({
            "company_id": company.company_id,
            "company_name": company.company_name,
            "selected_students": selected_count
        })

    return {
        "company_placements": result
    }