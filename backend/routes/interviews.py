from datetime import datetime

from flask import Blueprint, request

from extensions import db
from models.application import Application
from models.interview import Interview
from utils.decorators import token_required


interviews_bp = Blueprint(
    "interviews",
    __name__,
    url_prefix="/api/interviews"
)


@interviews_bp.route("", methods=["GET"])
@token_required
def get_interviews(payload):
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

        if not application_ids:
            interviews = []
        else:
            interviews = Interview.query.filter(
                Interview.application_id.in_(application_ids)
            ).order_by(Interview.interview_id).all()

    elif payload["role"] in ["TPO", "ADMIN", "SUPER_ADMIN"]:
        interviews = Interview.query.order_by(
            Interview.interview_id
        ).all()

    else:
        return {"error": "Access denied"}, 403

    return {
        "interviews": [
            {
                "interview_id": interview.interview_id,
                "application_id": interview.application_id,
                "round_name": interview.round_name,
                "scheduled_at": interview.scheduled_at.isoformat(),
                "mode": interview.mode,
                "result": interview.result,
                "remarks": interview.remarks
            }
            for interview in interviews
        ]
    }


@interviews_bp.route("", methods=["POST"])
@token_required
def schedule_interview(payload):
    if payload["role"] not in ["TPO", "ADMIN", "SUPER_ADMIN"]:
        return {
            "error": "Only TPO or admin can schedule interviews"
        }, 403

    data = request.get_json()

    if not data:
        return {
            "error": "Request body is required"
        }, 400

    application_id = data.get("application_id")
    round_name = data.get("round_name")
    scheduled_at = data.get("scheduled_at")
    mode = data.get("mode")

    if (
        not application_id
        or not round_name
        or not scheduled_at
        or not mode
    ):
        return {
            "error": "application_id, round_name, scheduled_at and mode are required"
        }, 400

    if mode not in ["ONLINE", "OFFLINE"]:
        return {
            "error": "Mode must be ONLINE or OFFLINE"
        }, 400

    try:
        scheduled_at = str(scheduled_at).strip()

        if scheduled_at.endswith("Z"):
            scheduled_at = scheduled_at[:-1]

        scheduled_at = datetime.fromisoformat(
            scheduled_at
        )

    except (TypeError, ValueError):
        return {
            "error": "scheduled_at must be a valid date and time"
        }, 400

    application = Application.query.get(application_id)

    if not application:
        return {
            "error": "Application not found"
        }, 404

    interview = Interview(
        application_id=application_id,
        round_name=round_name,
        scheduled_at=scheduled_at,
        mode=mode,
        result=data.get("result"),
        remarks=data.get("remarks")
    )

    db.session.add(interview)

    application.status = "INTERVIEW"

    db.session.commit()

    return {
        "message": "Interview scheduled successfully",
        "interview_id": interview.interview_id,
        "application_id": interview.application_id,
        "status": application.status
    }, 201