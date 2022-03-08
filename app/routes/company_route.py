from flask import Blueprint
from app.controllers import company_controller

bp = Blueprint("company", __name__, url_prefix="/company")

bp.get("")(company_controller.get_company)

bp.post("")(company_controller.post_company)
bp.post("/signin")(company_controller.signin_company)

bp.patch("")(company_controller.update_company)

bp.delete("")(company_controller.delete_company)

