from flask import Blueprint, request

from extensions import db
from models.company import Company
from utils.decorators import token_required


companies_bp = Blueprint("companies", __name__, url_prefix="/api/companies")


@companies_bp.route("", methods=["GET"])
@token_required
def get_companies(payload):
    companies = Company.query.order_by(Company.company_id).all()

    return {
        "companies": [
            {
                "company_id": company.company_id,
                "company_name": company.company_name,
                "industry": company.industry,
                "website": company.website,
                "location": company.location
            }
            for company in companies
        ]
    }


@companies_bp.route("", methods=["POST"])
@token_required
def create_company(payload):
    if payload["role"] not in ["TPO", "ADMIN", "SUPER_ADMIN"]:
        return {"error": "Only TPO or admin can create companies"}, 403

    data = request.get_json()

    if not data:
        return {"error": "Request body is required"}, 400

    company_name = data.get("company_name")

    if not company_name:
        return {"error": "company_name is required"}, 400

    company = Company(
        company_name=company_name,
        industry=data.get("industry"),
        website=data.get("website"),
        location=data.get("location")
    )

    db.session.add(company)
    db.session.commit()

    return {
        "message": "Company created successfully",
        "company_id": company.company_id
    }, 201