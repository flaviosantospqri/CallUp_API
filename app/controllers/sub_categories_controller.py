from app.models.subcategory_model import SubCategory
from flask import jsonify

from http import HTTPStatus

def get_all_subcategories():
    subcategories = SubCategory.query.all()

    if not subcategories.items():
        return {"error": "no data found"}, HTTPStatus.OK
    
    return jsonify(subcategories), HTTPStatus.OK
