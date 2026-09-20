from flask import Blueprint, request

from extensions import db
from models.student import Student
from models.job import Job
from models.application import Application
from utils.decorators import token_required


applications_bp = Blueprint(
    "applications",
    __name__,
    url_prefix="/api/applications"
)


@applications_bp.route("", methods=["GET"])
@token_required
def get_applications(payload):
    if payload["role"] == "STUDENT":
        student = Student.query.filter_by(
            user_id=payload["user_id"]
        ).first()

        if not student:
            return {"error": "Student profile not found"}, 404

        applications = Application.query.filter_by(
            student_id=student.student_id
        ).order_by(Application.application_id).all()

    elif payload["role"] in ["TPO", "ADMIN", "SUPER_ADMIN"]:
        applications = Application.query.order_by(
            Application.application_id
        ).all()

    else:
        return {"error": "Access denied"}, 403

    return {
        "applications": [
            {
                "application_id": application.application_id,
                "student_id": application.student_id,
                "student_name": application.student.full_name if application.student else None,
                "job_id": application.job_id,
                "job_title": application.job.job_title if application.job else None,
                "company_name": application.job.company.company_name if application.job and application.job.company else None,
                "status": application.status,
                "applied_at": application.applied_at.isoformat()
            }
            for application in applications
        ]
    }


@applications_bp.route("/<int:job_id>", methods=["POST"])
@token_required
def apply_for_job(payload, job_id):
    if payload["role"] != "STUDENT":
        return {"error": "Only students can apply for jobs"}, 403

    student = Student.query.filter_by(
        user_id=payload["user_id"]
    ).first()

    if not student:
        return {"error": "Student profile not found"}, 404

    job = Job.query.get(job_id)

    if not job:
        return {"error": "Job not found"}, 404

    if job.job_status != "OPEN":
        return {"error": "Job is not open for applications"}, 400

    existing_application = Application.query.filter_by(
        student_id=student.student_id,
        job_id=job.job_id
    ).first()

    if existing_application:
        return {"error": "Already applied for this job"}, 409

    if (
        job.minimum_cgpa is not None
        and (
            student.cgpa is None
            or student.cgpa < job.minimum_cgpa
        )
    ):
        return {"error": "Student does not meet the CGPA requirement"}, 403

    application = Application(
        student_id=student.student_id,
        job_id=job.job_id,
        status="APPLIED"
    )

    db.session.add(application)
    db.session.commit()

    return {
        "message": "Application submitted successfully",
        "application_id": application.application_id,
        "status": application.status
    }, 201


@applications_bp.route("/<int:application_id>/status", methods=["PUT"])
@token_required
def update_application_status(payload, application_id):
    if payload["role"] not in ["TPO", "ADMIN", "SUPER_ADMIN"]:
        return {"error": "Only TPO or admin can update application status"}, 403

    application = Application.query.get(application_id)

    if not application:
        return {"error": "Application not found"}, 404

    data = request.get_json()

    if not data:
        return {"error": "Request body is required"}, 400

    status = data.get("status")

    allowed_statuses = [
        "APPLIED",
        "SHORTLISTED",
        "INTERVIEW",
        "SELECTED",
        "REJECTED",
        "WITHDRAWN"
    ]

    if status not in allowed_statuses:
        return {
            "error": "Invalid application status",
            "allowed_statuses": allowed_statuses
        }, 400

    application.status = status

    db.session.commit()

    return {
        "message": "Application status updated successfully",
        "application_id": application.application_id,
        "status": application.status
    }