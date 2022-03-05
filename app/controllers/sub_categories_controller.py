from app.models.subcategory_model import SubCategory
from flask import jsonify

from http import HTTPStatus

def get_all_subcategories():
    subcategories = SubCategory.query.all()
    print(subcategories)

    if not subcategories:
        return {"error": "no data found"}, HTTPStatus.NOT_FOUND
    
    return jsonify(subcategories), HTTPStatus.OK