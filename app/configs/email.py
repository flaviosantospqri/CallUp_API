from flask import Flask
from flask_mail import Mail
from os import getenv


def init_app(app: Flask):
    mail_settings = {
        "MAIL_SERVER": getenv("MAIL_SERVER"),
        "MAIL_PORT": getenv("MAIL_PORT"),
        "MAIL_USERNAME": getenv("MAIL_USERNAME"),
        "MAIL_PASSWORD": getenv("MAIL_PASSWORD"),
        "MAIL_USE_TLS": True,
    }

    app.config.update(mail_settings)

    mail = Mail(app)

    app.mail = mail
