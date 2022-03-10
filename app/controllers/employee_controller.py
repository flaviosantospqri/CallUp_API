from concurrent.futures.process import _ExceptionWithTraceback
from email.policy import default
from sqlite3 import IntegrityError
from flask import request, jsonify, session
from http import HTTPStatus
from werkzeug.exceptions import NotFound, Unauthorized
from turtle import ht
from werkzeug.exceptions import BadRequest
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    create_access_token,
    jwt_required,
    get_jwt_identity,
)
from app.configs.database import db
from sqlalchemy.orm.session import Session
import re
from app.exc.provider_exc import PhoneFormatInvalidError

from app.models.company_model import Company
from app.models.sector_model import Sector

from app.models.employee_model import Employee

import re

session: Session = db.session


@jwt_required()
def get_employees():
    try:
        all_employees = session.query(Employee).all()
        current_user = get_jwt_identity()

        if current_user["type"] != "company":
            raise Unauthorized

        return jsonify(all_employees), HTTPStatus.OK

    except NotFound:
        return {"error": "no data found"}, HTTPStatus.NOT_FOUND

    except Unauthorized:
        return {"error": "access denied"}, HTTPStatus.UNAUTHORIZED


@jwt_required()
def post_employee():

    current_user = get_jwt_identity()

    if current_user["type"] != "company":
        return {"error": "access denied"}, HTTPStatus.BAD_REQUEST

    data = request.get_json()

    data["company_id"] = current_user["id"]

    for value in data.values():
        if type(value) != type("string"):
            return {
                "error": "All fields must be on string format"
            }, HTTPStatus.BAD_REQUEST

    default_keys = ["name", "email", "phone", "sector_id", "password"]

    for key in default_keys:
        if key not in data.keys():
            return {
                "error": f"Incomplete request, check {key} field"
            }, HTTPStatus.BAD_REQUES
    try:
        employee = Employee(**data)

        db.session.add(employee)
        db.session.commit()

    except BadRequest as e:
        return {str(e.description)}, HTTPStatus.BAD_REQUEST

    except IntegrityError:
        return {"error": "user already registred"}, HTTPStatus.CONFLICT

    return jsonify(employee), HTTPStatus.CREATED


@jwt_required()
def patch_employee(email):
    current_user = get_jwt_identity()

    if current_user["type"] != "company":
        return {"error": "access denied"}, HTTPStatus.UNAUTHORIZED

    try:
        data = request.get_json()

        columns = ["name", "phone"]

        valid_data = {item: data[item] for item in data if item in columns}

        current_employee = session.query(Employee).get(email)

        for key, value in valid_data.items():
            setattr(current_employee, key, value)

        session.add(current_employee)
        session.commit()

        return jsonify(current_employee), HTTPStatus.OK
    except BadRequest as e:
        return {str(e.description)}, HTTPStatus.BAD_REQUEST
    except NotFound:
        session.rollback()
        return {"error": "employee not found!"}, HTTPStatus.NOT_FOUND


@jwt_required()
def delete_employee(email):
    current_user = get_jwt_identity()

    if current_user["type"] != "company":
        return {"error": "access denied"}, HTTPStatus.BAD_REQUEST

    try:
        current_employee = session.query(Employee).get(email)

        session.delete(current_employee)

        session.commit()

        return {}, HTTPStatus.NO_CONTENT
    except:
        session.rollback()
        return {"error": "Not Found"}, HTTPStatus.NOT_FOUND


@jwt_required()
def find_employees(email):
    try:
        employee = session.query(Employee).filter_by(email=email).first_or_404()
        current_user = get_jwt_identity()

        if current_user["type"] != "company":
            return {"error": "access denied"}, HTTPStatus.BAD_REQUEST

        return jsonify(employee), HTTPStatus.OK

    except NotFound:
        return {"error": "no data found"}


def employee_login():
    data = request.get_json()
    try:

        employee: Employee = Employee.query.filter_by(email=data["email"]).first()

        if not employee or not employee.check_password(data["password"]):
            raise Unauthorized

        token = create_access_token(employee)

        return {"access_token": token}, HTTPStatus.ok

    except Unauthorized:
        return {"error": "E-mail and/or password incorrect."}, HTTPStatus.UNAUTHORIZED
