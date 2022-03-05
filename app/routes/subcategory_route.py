from flask import Blueprint
from app.controllers import sub_categories_controller

bp = Blueprint("sub_categories", __name__, url_prefix='/subcategories')

bp.get("")(sub_categories_controller.get_all_subcategories)