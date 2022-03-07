from flask import request, jsonify, current_app
from app.models.company_model import Company
import re
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError
from app.configs.database import db
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import UnmappedInstanceError
from flask_jwt_extended import (create_access_token, get_jwt_identity, jwt_required)

session: Session = db.session
# @jwt_required()
def get_companies():
    companies = Company.query.all()
    # companny = get_jwt_identity()
    if not companies:
        return {"error": "no data found"}, HTTPStatus.NOT_FOUND
    # return jsonify(companny), HTTPStatus.OK
    return jsonify(companies), HTTPStatus.OK

def post_company():
    data = request.get_json()

    default_keys = ["name", "cnpj", "address", "email","password"]

    for key in default_keys:
        if key not in data.keys():
            return {"error": f"Incomplete request, check {key} field"}, HTTPStatus.BAD_REQUEST 
    for key in data.keys():
        if key not in default_keys:
             return {"error": f"Incomplete request, check {key} field"}, HTTPStatus.BAD_REQUEST
    
    email_regex = "/^[a-z0-9._-]+@[a-z0-9]+.[a-z]+.([a-z]+)?$/i"
    validated_email = re.fullmatch(email_regex, data["email"])

    # if not validated_email:
    #     return {"error": "Wrong email format"}, HTTPStatus.BAD_REQUEST

    cnpj_regex = "/^([0-9]{3}\.?[0-9]{3}\.?[0-9]{3}\-?[0-9]{2}|[0-9]{2}\.?[0-9]{3}\.?[0-9]{3}\/?[0-9]{4}\-?[0-9]{2})$/"
    validate_cnpj = re.fullmatch(cnpj_regex, data["cnpj"])

    # if not validate_cnpj:
    #     return {"error": "Wrong CNPJ format"}, HTTPStatus.BAD_REQUEST

    try:
        company =  Company(**data)
        session.add(company)
        session.commit()
    except IntegrityError:
        return {"error": "company already registred"}, HTTPStatus.CONFLICT
    
    return jsonify(company), HTTPStatus.CREATED

def update_company():
    try: 
        data = request.get_json()

        company = Company.query.filter_by(cnpj=data['cnpj']).first()
        
        update_fields = ["name", "address"] 

        valid_data = {item: data[item] for item in data if item in update_fields}

        for key, value in valid_data.items():
            setattr(company, key, value)

        session.add(company)
        session.commit()
    except:
        session.rollback()
        return {'msg': 'company not found!'}, HTTPStatus.NOT_FOUND
    
    
    return jsonify(company), HTTPStatus.OK
           
def delete_company():
    try:
        data = request.get_json()

        company = Company.query.filter_by(cnpj=data['cnpj']).first()

        session.delete(company)
        session.commit()

        return "", HTTPStatus.OK
    except UnmappedInstanceError:
        return {"error": f"CNPJ: {data['cnpj']} do not found"}, HTTPStatus.NOT_FOUND

    
def signin_company():
    data = request.get_json()
    company: Company = Company.query.filter_by(email=data["email"]).first()
    if not company:
        return {"error": "email not found"}, HTTPStatus.NOT_FOUND
    if not company.check_password(data["password"]):
        return {"error": "email and password do not match"}, HTTPStatus.UNAUTHORIZED
    
    token = create_access_token(company)
    
    return {"token": token}, HTTPStatus.OK
