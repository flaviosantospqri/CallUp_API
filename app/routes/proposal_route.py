from flask import Blueprint
from app.controllers import proposal_controller

bp = Blueprint("proposal", __name__, url_prefix="/proposal")

bp.get("")(proposal_controller.get_proposals)
bp.get("")(proposal_controller.get_proposal_accepted)