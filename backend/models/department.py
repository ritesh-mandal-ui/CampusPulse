from extensions import db


class Department(db.Model):
    __tablename__ = "departments"

    department_id = db.Column(db.BigInteger, primary_key=True)
    department_name = db.Column(db.String(100), nullable=False)
    department_code = db.Column(db.String(20), unique=True, nullable=False)