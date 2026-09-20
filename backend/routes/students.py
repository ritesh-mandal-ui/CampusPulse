from datetime import datetime, timezone

from flask import Blueprint, request

from extensions import db
from models.student import Student
from models.skill import Skill
from models.student_skill import StudentSkill
from utils.decorators import token_required


students_bp = Blueprint("students", __name__, url_prefix="/api/students")


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