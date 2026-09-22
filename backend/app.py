from flask import Flask
from flask_cors import CORS

from config import Config
from extensions import db

from models.user import User
from models.student import Student
from models.password_reset_token import PasswordResetToken
from models.department import Department
from models.skill import Skill
from models.student_skill import StudentSkill
from models.company import Company
from models.job import Job
from models.application import Application
from models.interview import Interview
from models.offer import Offer

from routes.auth import auth_bp
from routes.students import students_bp
from routes.companies import companies_bp
from routes.jobs import jobs_bp
from routes.applications import applications_bp
from routes.interviews import interviews_bp
from routes.offers import offers_bp
from routes.analytics import analytics_bp
from routes.public import public_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)

    db.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(companies_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(applications_bp)
    app.register_blueprint(interviews_bp)
    app.register_blueprint(offers_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(public_bp)

    @app.route("/")
    def home():
        return {"message": "CampusPulse backend is running"}

    @app.route("/db-test")
    def db_test():
        try:
            db.session.execute(db.text("SELECT 1"))
            return {"message": "Database connection successful"}
        except Exception as e:
            return {"error": str(e)}, 500

    @app.route("/model-test")
    def model_test():
        try:
            user_count = db.session.query(User).count()
            student_count = db.session.query(Student).count()
            company_count = db.session.query(Company).count()
            job_count = db.session.query(Job).count()

            return {
                "message": "Models are working",
                "users": user_count,
                "students": student_count,
                "companies": company_count,
                "jobs": job_count
            }
        except Exception as e:
            return {"error": str(e)}, 500

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)