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

session: Session = db.session

@jwt_required
def get_employees():
    try:
        all_employees = session.query(Employee).all()
        current_user = get_jwt_identity()

        if current_user.type == 'employee':
            return {"error": "access denied"}

        if all_employees:
            return jsonify(all_employees), HTTPStatus.OK
    except: 
        return {"error": "no data found"}
def post_employee():
    ...
def patch_employee(email):
    ...
def delete_employee(email):
    ...
def find_employees(email):
    ... 
def employee_login():
    ...