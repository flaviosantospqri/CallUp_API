from app.controllers import sector_controller
from flask import Blueprint

bp_sector = Blueprint("sector", __name__, url_prefix="/sector")

bp_sector.get("")(sector_controller.get_all_sectors)