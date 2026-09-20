import os
import uuid
from datetime import datetime, timezone

from flask import Blueprint, request, send_file

from extensions import db
from models.student import Student
from models.skill import Skill
from models.student_skill import StudentSkill
from utils.decorators import token_required


students_bp = Blueprint("students", __name__, url_prefix="/api/students")

RESUME_FOLDER = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "uploads", "resumes")
)

MAX_RESUME_SIZE = 5 * 1024 * 1024


@students_bp.route("/profile", methods=["GET"])
@token_required
def profile(payload):
    student = Student.query.filter_by(user_id=payload["user_id"]).first()

    if not student:
        return {"error": "Student profile not found"}, 404

    return {
        "student_id": student.student_id,
        "user_id": student.user_id,
        "roll_number": student.roll_number,
        "full_name": student.full_name,
        "department_id": student.department_id,
        "cgpa": float(student.cgpa) if student.cgpa is not None else None,
        "graduation_year": student.graduation_year,
        "phone": student.phone,
        "resume_url": student.resume_url
    }


@students_bp.route("/profile", methods=["POST"])
@token_required
def create_profile(payload):
    if payload["role"] != "STUDENT":
        return {"error": "Only students can create a student profile"}, 403

    existing_student = Student.query.filter_by(
        user_id=payload["user_id"]
    ).first()

    if existing_student:
        return {"error": "Student profile already exists"}, 409

    data = request.get_json(silent=True)

    if not data:
        return {"error": "Request body is required"}, 400

    required_fields = [
        "roll_number",
        "full_name",
        "department_id"
    ]

    for field in required_fields:
        if not data.get(field):
            return {"error": f"{field} is required"}, 400

    student = Student(
        user_id=payload["user_id"],
        roll_number=data["roll_number"],
        full_name=data["full_name"],
        department_id=data["department_id"],
        cgpa=data.get("cgpa"),
        graduation_year=data.get("graduation_year"),
        phone=data.get("phone"),
        resume_url=data.get("resume_url"),
        created_at=datetime.now(timezone.utc)
    )

    db.session.add(student)
    db.session.commit()

    return {
        "message": "Student profile created successfully",
        "student_id": student.student_id
    }, 201


@students_bp.route("/resume", methods=["POST"])
@token_required
def upload_resume(payload):
    if payload["role"] != "STUDENT":
        return {"error": "Only students can upload resumes"}, 403

    student = Student.query.filter_by(
        user_id=payload["user_id"]
    ).first()

    if not student:
        return {"error": "Student profile not found"}, 404

    if "resume" not in request.files:
        return {"error": "Resume file is required"}, 400

    file = request.files["resume"]

    if not file or not file.filename:
        return {"error": "Resume file is required"}, 400

    if not file.filename.lower().endswith(".pdf"):
        return {"error": "Only PDF files are allowed"}, 400

    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)

    if file_size > MAX_RESUME_SIZE:
        return {"error": "Resume file must be 5 MB or smaller"}, 400

    os.makedirs(RESUME_FOLDER, exist_ok=True)

    filename = f"{uuid.uuid4().hex}.pdf"
    file_path = os.path.join(RESUME_FOLDER, filename)

    file.save(file_path)

    if student.resume_url:
        old_filename = os.path.basename(student.resume_url)
        old_file_path = os.path.join(RESUME_FOLDER, old_filename)

        if os.path.isfile(old_file_path):
            os.remove(old_file_path)

    student.resume_url = f"/api/students/resume/{filename}"
    db.session.commit()

    return {
        "message": "Resume uploaded successfully",
        "resume_url": student.resume_url
    }, 200


@students_bp.route("/resume/<filename>", methods=["GET"])
@token_required
def download_resume(payload, filename):
    if payload["role"] != "STUDENT":
        return {"error": "Only students can access resumes"}, 403

    student = Student.query.filter_by(
        user_id=payload["user_id"]
    ).first()

    if not student:
        return {"error": "Student profile not found"}, 404

    expected_filename = os.path.basename(student.resume_url or "")

    if not expected_filename or filename != expected_filename:
        return {"error": "Resume not found"}, 404

    file_path = os.path.join(RESUME_FOLDER, filename)

    if not os.path.isfile(file_path):
        return {"error": "Resume file not found"}, 404

    return send_file(
        file_path,
        mimetype="application/pdf",
        as_attachment=False,
        download_name="resume.pdf"
    )


@students_bp.route("/available-skills", methods=["GET"])
@token_required
def get_available_skills(payload):
    skills = Skill.query.order_by(Skill.skill_name).all()

    return {
        "skills": [
            {
                "skill_id": skill.skill_id,
                "skill_name": skill.skill_name
            }
            for skill in skills
        ]
    }


@students_bp.route("/skills", methods=["GET"])
@token_required
def get_skills(payload):
    student = Student.query.filter_by(user_id=payload["user_id"]).first()

    if not student:
        return {"error": "Student profile not found"}, 404

    student_skills = StudentSkill.query.filter_by(
        student_id=student.student_id
    ).all()

    skills = []

    for student_skill in student_skills:
        skill = Skill.query.get(student_skill.skill_id)

        if skill:
            skills.append({
                "skill_id": skill.skill_id,
                "skill_name": skill.skill_name,
                "proficiency": student_skill.proficiency
            })

    return {
        "student_id": student.student_id,
        "skills": skills
    }


@students_bp.route("/skills", methods=["POST"])
@token_required
def add_skill(payload):
    if payload["role"] != "STUDENT":
        return {"error": "Only students can add skills"}, 403

    student = Student.query.filter_by(user_id=payload["user_id"]).first()

    if not student:
        return {"error": "Student profile not found"}, 404

    data = request.get_json(silent=True)

    if not data:
        return {"error": "Request body is required"}, 400

    skill_id = data.get("skill_id")
    proficiency = data.get("proficiency")

    if not skill_id:
        return {"error": "skill_id is required"}, 400

    skill = Skill.query.get(skill_id)

    if not skill:
        return {"error": "Skill not found"}, 404

    existing_skill = StudentSkill.query.filter_by(
        student_id=student.student_id,
        skill_id=skill_id
    ).first()

    if existing_skill:
        return {"error": "Skill already added"}, 409

    student_skill = StudentSkill(
        student_id=student.student_id,
        skill_id=skill_id,
        proficiency=proficiency
    )

    db.session.add(student_skill)
    db.session.commit()

    return {
        "message": "Skill added successfully",
        "skill_id": skill.skill_id,
        "skill_name": skill.skill_name,
        "proficiency": proficiency
    }, 201