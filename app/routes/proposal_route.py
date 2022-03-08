from flask import Blueprint
from app.controllers import proposal_controller

bp = Blueprint("proposal", __name__, url_prefix="/proposal")

bp.get("")(proposal_controller.get_proposals)
bp.get("")(proposal_controller.get_proposal_accepted)


bp.post("")(proposal_controller.create_proposal)

bp.patch("/<proposal_id>")(proposal_controller.update_proposal)

bp.delete("/<proposal_id>")(proposal_controller.delete_proposal)
