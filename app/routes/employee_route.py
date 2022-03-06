from app.controllers import employee_controller
from flask import Blueprint

bp = Blueprint("employee", __name__, url_prefix="/employee")

bp.get("")(employee_controller.get_employees)
bp.post("")(employee_controller.post_employee)
bp.get("/<id>")(employee_controller.find_employees)
bp.patch("/<id>")(employee_controller.patch_employee)
bp.delete("/<id>")(employee_controller.delete_employee)
