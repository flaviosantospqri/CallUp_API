from concurrent.futures.process import _ExceptionWithTraceback
from email.policy import default
from flask import request, jsonify, session
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import NotFound
from app.configs.database import db
from sqlalchemy.orm.session import Session
import re

from app.models.company_model import Company
from app.models.sector_model import Sector

from app.models.employee_model import Employee

session: Session = db.session


@jwt_required
def get_employees():
    ...


def post_employee():
    ...


@jwt_required
def patch_employee(email):
    current_user = get_jwt_identity()

    if current_user.type != "company":
        return {"error": "access denied"}, HTTPStatus.UNAUTHORIZED
    default = (
        "^(([1-9]{2})[9]{1}[0-9]{4}-[0-9]{4})|(([1-9]{2})[1-9]{1}[0-9]{3}-[0-9]{4})$"
    )
    try:
        data = request.get_json()

        columns = ["name", "phone"]

        correct_phone_value = re.fullmatch(default, data["phone"])

        if not correct_phone_value:
            return {"msg": "phone format is invalid"}, HTTPStatus.BAD_REQUEST

        valid_data = {item: data[item] for item in data if item in columns}

        current_employee = session.query(Employee).get(email)

        for key, value in valid_data.items():
            setattr(current_employee, key, value)

        session.add(current_employee)
        session.commit()

        return jsonify(current_employee), HTTPStatus.OK
    except NotFound:
        session.rollback()
        return {"msg": "employee not found!"}, HTTPStatus.NOT_FOUND


def delete_employee(email):
    ...


def find_employees(email):
    ...


def employee_login():
    ...
