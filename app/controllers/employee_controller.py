from sqlite3 import IntegrityError
from flask import request, jsonify, session
from http import HTTPStatus
from werkzeug.exceptions import NotFound, Unauthorized
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

from app.models.company_model import Company
from app.models.sector_model import Sector

from app.models.employee_model import Employee


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

    try:

        if current_user["type"] != "company":
            raise BadRequest(descprition={"error": "access denied"})

        data = request.get_json()

        sector_name = data.pop('sector')
        company_id = current_user["id"]

        sector: Sector = (
                session.query(Sector)
                .filter_by(name=sector_name)
                .first_or_404(description={"error": "category doesn't exist"})
            )

        company: Company = (
                session.query(Company)
                .get_or_404(company_id,description={"error": "category doesn't exist"})
            )

        valid_data = Employee.check_fields(data)

        employee = Employee(**valid_data)

        sector.employees.append(employee)
        company.employees.append(employee)

        session.add(employee)
        session.commit()

        return jsonify(employee), HTTPStatus.CREATED

    except BadRequest as e:
        return e.description, HTTPStatus.BAD_REQUEST

    except IntegrityError:
        return {"error": "user already registred"}, HTTPStatus.CONFLICT




@jwt_required()
def patch_employee(email):
    current_user = get_jwt_identity()

    try:
        if current_user["type"] != "company":
            raise Unauthorized

        current_company = session.query(Company).get(current_user["id"])

        current_employee = session.query(Employee).filter_by(email=email).first_or_404()

        if current_employee not in current_company.employees:
            raise Unauthorized

        data = request.get_json()

        valid_data = Employee.check_data_for_update(data)
        
        if "category" in data:
            sector_name = data.pop('sector')
            current_employee.sector_id = None

            sector: Sector = (
                session.query(Sector)
                .filter_by(name=sector_name)
                .first_or_404(description={"error": "category doesn't exist"})
            )

            sector.append(current_employee)

        for key, value in valid_data.items():
            setattr(current_employee, key, value)

        session.add(current_employee)
        session.commit()

        return jsonify(current_employee), HTTPStatus.OK

    except BadRequest as e:
        return e.description, HTTPStatus.BAD_REQUEST

    except NotFound:
        session.rollback()
        return {"error": "employee not found!"}, HTTPStatus.NOT_FOUND

    except Unauthorized:
        return {"error": "access denied"}, HTTPStatus.UNAUTHORIZED


@jwt_required()
def delete_employee(email):
    current_user = get_jwt_identity()

    try:
        if current_user["type"] != "company":
            raise Unauthorized

        current_company = session.query(Company).get(current_user["id"])

        current_employee = session.query(Employee).filter_by(email=email).first_or_404()

        if current_employee not in current_company.employees:
            raise Unauthorized

        session.delete(current_employee)

        session.commit()

        return {}, HTTPStatus.NO_CONTENT

    except NotFound:
        session.rollback()
        return {"error": "employee not found!"}, HTTPStatus.NOT_FOUND

    except Unauthorized:
        return {"error": "access denied"}, HTTPStatus.UNAUTHORIZED


@jwt_required()
def find_employees(email):
    try:
        current_user = get_jwt_identity()

        if current_user["type"] != "company":
            raise Unauthorized
        
        current_company = session.query(Company).get(current_user["id"])

        employee = session.query(Employee).filter_by(email=email).first_or_404()

        if employee not in current_company.employees:
            raise Unauthorized
        
        return jsonify(employee), HTTPStatus.OK

    except NotFound:
        session.rollback()
        return {"error": "employee not found!"}, HTTPStatus.NOT_FOUND

    except Unauthorized:
        return {"error": "access denied"}, HTTPStatus.UNAUTHORIZED


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
