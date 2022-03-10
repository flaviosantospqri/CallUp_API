from flask import jsonify, request
from http import HTTPStatus
from app.exc.provider_exc import (
    CnpjFormatInvalidError,
    EmailFormatInvalidError,
    PasswordFormatinvalidError,
)
from app.models.provider_model import Provider
from werkzeug.exceptions import NotFound, Unauthorized
from sqlalchemy.orm.exc import UnmappedInstanceError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.configs.database import db
from sqlalchemy.exc import IntegrityError
import re


def get_providers():
    providers = Provider.query.all()

    return jsonify(providers), HTTPStatus.OK


def get_provider_by_id(provider_id):
    try:
        provider = Provider.query.filter_by(cidnpj=provider_id).first_or_404()

        return jsonify(provider), HTTPStatus.OK

    except NotFound:

        return {"error": "no provider found"}, HTTPStatus.NOT_FOUND


@jwt_required()
def patch_provider():

    token_user = get_jwt_identity()

    if token_user["type"] != "provider":
        raise Unauthorized

    try:

        data = request.get_json()

        provider: Provider = Provider.query.filter_by(
            id=token_user["id"]
        ).first_or_404()

        allowed_columns = ["name", "about"]

        valid_data = {item: data[item] for item in data if item in allowed_columns}

        for key, value in valid_data.items():
            setattr(provider, key, value)

        db.session.add(provider)
        db.session.commit()

        return jsonify(provider), HTTPStatus.OK

    except Unauthorized:

        return {"error": "access denied"}, HTTPStatus.UNAUTHORIZED

    except NotFound:

        return {"error": "no data found"}, HTTPStatus.NOT_FOUND


def create_provider():
    session = db.session

    data = request.get_json()

    Provider.check_fields(data)

    password_regex = re.compile(r"^(((?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%<^&*?])[a-zA-Z0-9!@#$%<^&*?]{8,})|([a-zA-Z]+([- .,_][a-zA-Z]+){4,}))$")
    validate_password = re.fullmatch(password_regex, data['password'])
    if not validate_password:
        return {"error": "Invalid password format. A good password should be at least 8 characters long: letters, numbers and special characters. Example: Potato1@"}, HTTPStatus.BAD_REQUEST
    
    try:
        provider = Provider(**data)
        session.add(provider)
        session.commit()

    except IntegrityError:
        return {"error": f"Provider already registred"}, HTTPStatus.CONFLICT

    except CnpjFormatInvalidError:
        return {"error": "CNPJ format invalid. Format valid 00.000.000/0000-00 or 00000000000000"}, HTTPStatus.BAD_REQUEST


    except EmailFormatInvalidError:
        return {"error": "Email format invalid. Format valid example@mail.com"}, HTTPStatus.BAD_REQUEST

    except PasswordFormatinvalidError:
        return {"error": "Password format invalid. Use at least aA@1, examplo Batat@1"}, HTTPStatus.BAD_REQUEST



    return jsonify(provider), HTTPStatus.CREATED


def login_provider():

    data = request.get_json()

    try:
        provider: Provider = (Provider.query.filter_by(email=data["email"])).first()

        if not provider or not provider.password_check(data["password"]):
            raise Unauthorized

        token = create_access_token(provider)

        return {"token": token}, HTTPStatus.OK
    
    except Unauthorized:

        return {"error": "E-mail and/or password incorrect."}, HTTPStatus.UNAUTHORIZED



@jwt_required()
def delete_provider():

    session = db.session
    current_provider = get_jwt_identity()

    try:
        provider = Provider.query.get_or_404(current_provider["id"])

        session.delete(provider)
        session.commit()

        return "", HTTPStatus.OK

    except NotFound:
        return {"error": "Provider not found"}, HTTPStatus.NOT_FOUND
