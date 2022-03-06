from concurrent.futures.process import _ExceptionWithTraceback
from flask import request, jsonify, session
from http import HTTPStatus


from app.configs.database import db
from sqlalchemy.orm.session import Session

from sqlalchemy.exc import IntegrityError
from app.models.company_model import Company
from app.models.sector_model import Sector

from app.models.employee_model import Employee

session: Session = db.session

def get_employees():
    try:
        all_employees = session.query(Employee).all()

        if all_employees:
            return jsonify(all_employees), HTTPStatus.OK
    except: 
        return {"error": "no data found"}
def post_employee():
    ...
def patch_employee(id):
    ...
def delete_employee(id):
    ...
def find_employees(id):
    ... 