from flask import Blueprint
from app.controllers.pdf_controller import send_pdf

bp = Blueprint("pb_pdf", __name__, url_prefix="/pdfreport")

bp.get("")(send_pdf)