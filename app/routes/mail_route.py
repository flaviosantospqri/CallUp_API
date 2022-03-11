from flask import Blueprint
from app.controllers.mail_controller import send_mail

bp = Blueprint("pb_mail", __name__)

bp.get("")(send_mail)
