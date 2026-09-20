from flask import Blueprint, request

from extensions import db
from models.job import Job
from models.company import Company
from utils.decorators import token_required


jobs_bp = Blueprint("jobs", __name__, url_prefix="/api/jobs")


@jobs_bp.route("", methods=["GET"])
@token_required
def get_jobs(payload):
    jobs = Job.query.order_by(Job.job_id).all()

    return {
        "jobs": [
            {
                "job_id": job.job_id,
                "company_id": job.company_id,
                "company_name": job.company.company_name if job.company else None,
                "job_title": job.job_title,
                "job_description": job.job_description,
                "minimum_cgpa": float(job.minimum_cgpa) if job.minimum_cgpa is not None else None,
                "maximum_backlogs": job.maximum_backlogs,
                "salary_lpa": float(job.salary_lpa) if job.salary_lpa is not None else None,
                "application_deadline": job.application_deadline.isoformat() if job.application_deadline else None,
                "job_status": job.job_status,
                "created_by": job.created_by
            }
            for job in jobs
        ]
    }


@jobs_bp.route("", methods=["POST"])
@token_required
def create_job(payload):
    if payload["role"] not in ["TPO", "ADMIN", "SUPER_ADMIN"]:
        return {"error": "Only TPO or admin can create jobs"}, 403

    data = request.get_json()

    if not data:
        return {"error": "Request body is required"}, 400

    required_fields = [
        "company_id",
        "job_title"
    ]

    for field in required_fields:
        if not data.get(field):
            return {"error": f"{field} is required"}, 400

    company = Company.query.get(data["company_id"])

    if not company:
        return {"error": "Company not found"}, 404

    job_status = data.get("job_status", "OPEN")

    if job_status not in ["OPEN", "CLOSED", "CANCELLED"]:
        return {
            "error": "Job status must be OPEN, CLOSED or CANCELLED"
        }, 400

    job = Job(
        company_id=data["company_id"],
        job_title=data["job_title"],
        job_description=data.get("job_description"),
        minimum_cgpa=data.get("minimum_cgpa"),
        maximum_backlogs=data.get("maximum_backlogs", 0),
        salary_lpa=data.get("salary_lpa"),
        application_deadline=data.get("application_deadline"),
        job_status=job_status,
        created_by=payload["user_id"]
    )

    db.session.add(job)
    db.session.commit()

    return {
        "message": "Job created successfully",
        "job_id": job.job_id
    }, 201