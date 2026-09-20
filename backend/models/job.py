from datetime import datetime, timezone

from extensions import db


class Job(db.Model):
    __tablename__ = "jobs"

    job_id = db.Column(db.BigInteger, primary_key=True)
    company_id = db.Column(
        db.BigInteger,
        db.ForeignKey("companies.company_id", ondelete="CASCADE"),
        nullable=False
    )
    job_title = db.Column(db.String(150), nullable=False)
    job_description = db.Column(db.Text)
    minimum_cgpa = db.Column(db.Numeric(3, 2))
    maximum_backlogs = db.Column(db.Integer, default=0)
    salary_lpa = db.Column(db.Numeric(8, 2))
    application_deadline = db.Column(db.DateTime)
    job_status = db.Column(db.String(30))
    created_by = db.Column(
        db.BigInteger,
        db.ForeignKey("users.user_id")
    )
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    company = db.relationship("Company")