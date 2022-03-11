from flask import Blueprint
from app.controllers import call_controller

bp = Blueprint("call", __name__, url_prefix="/calls")

bp.get("")(call_controller.get_call)
bp.get("/<id>")(call_controller.get_call_id)

bp.post("")(call_controller.post_call)

bp.patch("/<id>")(call_controller.update_call)
bp.patch("/call_id/close")(call_controller.close_call)

bp.delete("/<id>")(call_controller.delete_call)
