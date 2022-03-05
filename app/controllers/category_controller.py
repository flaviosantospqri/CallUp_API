from flask import jsonify
from app.models.category_model import Category

from http import HTTPStatus

def get_categories():
    categories = Category.query.all()

    if not categories:
        return {"error": "no data found"}, HTTPStatus.NOT_FOUND

    return jsonify(categories.items), HTTPStatus.OK