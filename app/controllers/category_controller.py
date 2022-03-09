from flask import jsonify
from app.models.category_model import Category

from http import HTTPStatus

def get_categories():
    categories = Category.query.all()

    return jsonify(categories), HTTPStatus.OK