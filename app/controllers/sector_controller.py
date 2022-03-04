from app.models.sector_model import Sector
from flask import jsonify

from http import HTTPStatus

def get_all_sectors():
    sectors = Sector.query.all()

    if not sectors.items():
        return {"error": "no data found"}, HTTPStatus.OK

    return jsonify(sectors), HTTPStatus.OK