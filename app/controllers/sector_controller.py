from app.models.sector_model import Sector
from flask import jsonify

from http import HTTPStatus


def get_all_sectors():
    sectors = Sector.query.all()

    return jsonify(sectors), HTTPStatus.OK
