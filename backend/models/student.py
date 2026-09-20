from datetime import datetime, timezone

from extensions import db


class Student(db.Model):
    __tablename__ = "students"

    student_id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(
        db.BigInteger,
        db.ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )
    roll_number = db.Column(db.String(50), unique=True, nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    department_id = db.Column(
        db.BigInteger,
        db.ForeignKey("departments.department_id"),
        nullable=False
    )
    cgpa = db.Column(db.Numeric(3, 2))
    graduation_year = db.Column(db.Integer)
    phone = db.Column(db.String(20))
    resume_url = db.Column(db.Text)
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )