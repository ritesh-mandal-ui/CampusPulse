from extensions import db


class StudentSkill(db.Model):
    __tablename__ = "student_skills"

    student_id = db.Column(
        db.BigInteger,
        db.ForeignKey("students.student_id", ondelete="CASCADE"),
        primary_key=True
    )
    skill_id = db.Column(
        db.BigInteger,
        db.ForeignKey("skills.skill_id", ondelete="CASCADE"),
        primary_key=True
    )
    proficiency = db.Column(db.String(30))