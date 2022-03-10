from flask import request, jsonify, current_app
from app.exc.provider_exc import (
    CnpjFormatInvalidError,
    EmailFormatInvalidError,
    PasswordFormatinvalidError,
)
from app.models.company_model import Company
import re
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError
from app.configs.database import db
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import UnmappedInstanceError
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

session: Session = db.session


@jwt_required()
def get_company():

    company: Company = get_jwt_identity()
    if not company:
        return {"error": "no data found"}, HTTPStatus.NOT_FOUND

    return jsonify(company), HTTPStatus.OK


def post_company():
    data = request.get_json()

    Company.check_fields(data)

    password_regex = re.compile(
        r"^(((?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%<^&*?])[a-zA-Z0-9!@#$%<^&*?]{8,})|([a-zA-Z]+([- .,_][a-zA-Z]+){4,}))$"
    )
    validate_password = re.fullmatch(password_regex, data["password"])
    if not validate_password:
        return {"error": "Wrong password format"}, HTTPStatus.BAD_REQUEST

    try:
        company = Company(**data)
        session.add(company)
        session.commit()
    except IntegrityError:
        return {"error": "company already registred"}, HTTPStatus.CONFLICT
    except CnpjFormatInvalidError:
        return {"error": "Wrong CNPJ format"}, HTTPStatus.BAD_REQUEST
    except EmailFormatInvalidError:
        return {"error": "Wrong email format"}, HTTPStatus.BAD_REQUEST
    except PasswordFormatinvalidError:
        return {"error": "Wrong password format"}, HTTPStatus.BAD_REQUEST
    return jsonify(company), HTTPStatus.CREATED


@jwt_required()
def update_company():
    try:
        data = request.get_json()
        # company = Company.query.filter_by(cnpj=data['cnpj']).first()
        current_user = get_jwt_identity()
        company = session.query(Company).filter_by(cnpj=current_user["cnpj"]).first()

        update_fields = ["name", "address"]
        valid_data = {item: data[item] for item in data if item in update_fields}

        for key, value in valid_data.items():
            setattr(company, key, value)

        session.add(company)
        session.commit()
    except:
        session.rollback()
        return {"msg": "company not found!"}, HTTPStatus.NOT_FOUND

    return jsonify(company), HTTPStatus.OK


def delete_company():
    try:
        data = request.get_json()

        company = Company.query.filter_by(cnpj=data["cnpj"]).first()

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
