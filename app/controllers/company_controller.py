from flask import request, jsonify, current_app
from app.models.company_model import Company

from http import HTTPStatus

def get_companies():
    companies = Company.query.all()

    if not companies:
        return {"error": "no data found"}, HTTPStatus.NOT_FOUND

    return jsonify(companies), HTTPStatus.OK

def get_company_by_id(company_id:int):
    company = Company.query.get(company_id)

    if not company:
        return {"error": f"company id {company_id} not found"}, HTTPStatus.NOT_FOUND

    return jsonify(company), HTTPStatus.OK

