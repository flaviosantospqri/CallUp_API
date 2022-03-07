from flask import Blueprint
from app.controllers import company_controller

bp = Blueprint("company", __name__, url_prefix="/company")

bp.get("")(company_controller.get_companies)
