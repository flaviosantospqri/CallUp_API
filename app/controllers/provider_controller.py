from flask import jsonify
from http import HTTPStatus
from app.models.provider_model import Provider
from werkzeug.exceptions import NotFound

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
    