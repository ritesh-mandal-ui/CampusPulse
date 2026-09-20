from extensions import db


class Company(db.Model):
    __tablename__ = "companies"

    company_id = db.Column(db.BigInteger, primary_key=True)
    company_name = db.Column(db.String(150), nullable=False)
    industry = db.Column(db.String(100))
    website = db.Column(db.Text)
    location = db.Column(db.String(150))