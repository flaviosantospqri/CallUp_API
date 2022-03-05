from flask import Blueprint
from app.controllers import subcategory_controller

bp = Blueprint("sub_categories", __name__, url_prefix='/subcategories')

bp.get("")(subcategory_controller.get_all_subcategories)