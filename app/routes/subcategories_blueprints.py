from flask import Blueprint
from app.controllers import sub_categories_controller

bp_sub_category = Blueprint("sub_categories", __name__, url_prefix='/subcategories')

bp_sub_category.get("")(sub_categories_controller.get_all_subcategories)