from flask import jsonify, request
from http import HTTPStatus
from app.exc.provider_exc import CnpjFormatInvalidError, EmailFormatInvalidError, PasswordFormatinvalidError
from app.models.provider_model import Provider
from werkzeug.exceptions import NotFound, Unauthorized
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.configs.database import db
from app.services.provider_service import validate_cnpj, validate_email, validate_password

def get_providers():
    providers = Provider.query.all()

    if not providers:
        return {"error": "no data found"}, HTTPStatus.NOT_FOUND

    return jsonify(providers), HTTPStatus.OK

def get_provider_by_cnpj(provider_cnpj):
    try:
        provider = Provider.query.filter_by(cnpj=provider_cnpj).first_or_404()

        return jsonify(provider), HTTPStatus.OK

    except NotFound:

        return {"error": f"no provider with the CNPJ {provider_cnpj} found"}, HTTPStatus.NOT_FOUND

@jwt_required()
def patch_provider():

    token_user = get_jwt_identity()

    if token_user.type != 'provider':
        return {"error": "access denied"}, HTTPStatus.BAD_REQUEST

    try:

        data = request.get_json()

        provider: Provider = Provider.query.filter_by(cnpj=token_user.cnpj).first_or_404()

        allowed_columns = ['name', 'about']

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


def post_provider():
    session = db.session

    data = request.get_json()
    
    try:
        validate_password(data["password"])
        data["cnpj"] = validate_cnpj(data["cnpj"])

        print(data["cnpj"])

        new_provider = Provider(**data)
        validate_email(new_provider.email)

    except CnpjFormatInvalidError:
        return {"error": "CNPJ format invalid. Format valid 00.000.000/0000-00 or 00000000000000"}

    except EmailFormatInvalidError:
        return {"error": "Email format invalid. Format valid example@mail.com"}

    except PasswordFormatinvalidError:
        return {"error": "Password format invalid. Use at least aA@1, examplo Batat@1"}

    session.add(new_provider)
    session.commit()

    return jsonify(new_provider), HTTPStatus.CREATED