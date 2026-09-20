from extensions import db


class Interview(db.Model):
    __tablename__ = "interviews"

    interview_id = db.Column(db.BigInteger, primary_key=True)
    application_id = db.Column(
        db.BigInteger,
        db.ForeignKey("applications.application_id", ondelete="CASCADE"),
        nullable=False
    )
    round_name = db.Column(db.String(100))
    scheduled_at = db.Column(db.DateTime, nullable=False)
    mode = db.Column(db.String(30))
    result = db.Column(db.String(30))
    remarks = db.Column(db.Text)