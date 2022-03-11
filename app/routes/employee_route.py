from app.controllers import employee_controller
from flask import Blueprint

bp = Blueprint("employee", __name__, url_prefix="/employees")

bp.get("")(employee_controller.get_employees)
bp.post("")(employee_controller.post_employee)
bp.get("/<email>")(employee_controller.find_employees)
bp.patch("/<email>")(employee_controller.patch_employee)
bp.delete("/<email>")(employee_controller.delete_employee)
bp.post("/login")(employee_controller.employee_login)
