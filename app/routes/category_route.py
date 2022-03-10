from flask import Blueprint
from app.controllers import category_controller

bp = Blueprint("categories", __name__, url_prefix="/categories")

bp.get("")(category_controller.get_categories)
