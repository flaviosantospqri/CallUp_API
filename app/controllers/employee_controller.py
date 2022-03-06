from concurrent.futures.process import _ExceptionWithTraceback
from flask import request, jsonify, session
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.configs.database import db
from sqlalchemy.orm.session import Session

from sqlalchemy.exc import IntegrityError
from app.models.company_model import Company
from app.models.sector_model import Sector

from app.models.employee_model import Employee

import re

session: Session = db.session

@jwt_required
def get_employees():
    try:
        all_employees = session.query(Employee).all()
        current_user = get_jwt_identity()

        if current_user.type != 'company':
            return {"error": "access denied"}, HTTPStatus.BAD_REQUEST

        if all_employees:
            return jsonify(all_employees), HTTPStatus.OK
    except: 
        return {"error": "no data found"}

@jwt_required
def post_employee():

    current_user = get_jwt_identity()

    if current_user.type != 'company':
        return {"error": "access denied"}, HTTPStatus.BAD_REQUEST

    data = request.get_json()

    data['company_id'] = current_user.id

    for value in data.values():
        if type(value) != type("string"):
            return {"error": "All fields must be on string format"}, HTTPStatus.BAD_REQUEST
    
    default_keys = ["name", "email", "phone", "sector"]

    for key in default_keys:
        if key not in data.keys():
            return {"error": f"Incomplete request, check {key} field"}, HTTPStatus.BAD_REQUEST

    for key in data.keys():
        if key not in default_keys:
            return {"error": f"Incomplete request, check {key} field"}, HTTPStatus.BAD_REQUEST

    phone_regex = "^(([1-9]{2})[9]{1}[0-9]{4}-[0-9]{4})|(([1-9]{2})[1-9]{1}[0-9]{3}-[0-9]{4})$"
    validated_phone = re.fullmatch(phone_regex, data["phone"])

    if not validated_phone:
        return {"error": "Wrong phone format"}, HTTPStatus.BAD_REQUEST

    email_regex = "/^[a-z0-9._-]+@[a-z0-9]+.[a-z]+.([a-z]+)?$/i"
    validated_email = re.fullmatch(email_regex, data["email"])

    if not validated_email:
        return {"error": "Wrong email format"}, HTTPStatus.BAD_REQUEST

    try:
        employee = Employee(**data)

        db.session.add(employee)
        db.session.commit()

    except IntegrityError:
        return {"error": "user already registred"}, HTTPStatus.CONFLICT
    
    return jsonify(employee), HTTPStatus.CREATED

def patch_employee(email):
    ...
def delete_employee(email):
    ...
def find_employees(email):
    ... 
def employee_login():
    ...