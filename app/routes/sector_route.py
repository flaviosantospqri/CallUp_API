from app.controllers import sector_controller
from flask import Blueprint

bp = Blueprint("sector", __name__, url_prefix="/sector")

bp.get("")(sector_controller.get_all_sectors)