from flask import Blueprint
from app.controllers import company_controller

bp = Blueprint("company", __name__, url_prefix="/companies")

bp.get("")(company_controller.get_company)
bp.get("/pdf")(company_controller.send_pdf)

bp.post("")(company_controller.post_company)
bp.post("/login")(company_controller.signin_company)

bp.patch("")(company_controller.update_company)

bp.delete("")(company_controller.delete_company)


