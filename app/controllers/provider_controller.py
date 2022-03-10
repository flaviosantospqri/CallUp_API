from flask import jsonify, request
from http import HTTPStatus
from app.models.provider_model import Provider
from werkzeug.exceptions import NotFound, Unauthorized
from sqlalchemy.orm.exc import UnmappedInstanceError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.configs.database import db
from sqlalchemy.exc import IntegrityError
import re
from werkzeug.exceptions import BadRequest


def get_providers():
    providers = Provider.query.all()

    return jsonify(providers), HTTPStatus.OK


def get_provider_by_cnpj(provider_cnpj):
    try:
        provider = Provider.query.filter_by(cnpj=provider_cnpj).first_or_404()

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

        valid_data = Provider.check_data_for_update(data)

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

    try:
        provider = Provider(**data)
        session.add(provider)
        session.commit()

    except IntegrityError:
        return {"error": f"Provider already registred"}, HTTPStatus.CONFLICT

    except BadRequest as e:
        return {str(e.description)}, HTTPStatus.BAD_REQUEST
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
