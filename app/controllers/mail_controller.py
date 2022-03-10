from http import HTTPStatus
from flask import current_app, render_template
from flask_mail import Message, Mail
from os import getenv
from flask_jwt_extended import get_jwt_identity, jwt_required


@jwt_required()
def send_mail():
    mail: Mail = current_app.mail
    msg = Message(
        subject="Titulo do email",
        sender=getenv("MAIL_USERNAME"),
        recipients=["destinatario@mail.com"],
        html=render_template("email/template.html"),
    )

    mail.send(msg)

    return {"stts": "ok"}, 200
