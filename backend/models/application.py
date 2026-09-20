from datetime import datetime, timezone

from extensions import db


class Application(db.Model):
    __tablename__ = "applications"

    application_id = db.Column(db.BigInteger, primary_key=True)
    student_id = db.Column(
        db.BigInteger,
        db.ForeignKey("students.student_id", ondelete="CASCADE"),
        nullable=False
    )
    job_id = db.Column(
        db.BigInteger,
        db.ForeignKey("jobs.job_id", ondelete="CASCADE"),
        nullable=False
    )
    status = db.Column(db.String(30), nullable=False, default="APPLIED")
    applied_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    student = db.relationship("Student")
    job = db.relationship("Job")