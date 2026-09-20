from extensions import db


class Offer(db.Model):
    __tablename__ = "offers"

    offer_id = db.Column(db.BigInteger, primary_key=True)
    application_id = db.Column(
        db.BigInteger,
        db.ForeignKey("applications.application_id", ondelete="CASCADE"),
        nullable=False
    )
    salary_lpa = db.Column(db.Numeric(8, 2), nullable=False)
    offer_date = db.Column(db.Date, nullable=False)
    offer_status = db.Column(
        db.String(30),
        nullable=False,
        default="ACTIVE"
    )