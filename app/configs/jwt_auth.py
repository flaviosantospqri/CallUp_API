from flask import Flask
from flask_jwt_extended import JWTManager
from os import getenv
from datetime import timedelta


def init_app(app: Flask):
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=60)
    app.config["JWT_SECRET_KEY"] = getenv("SECRET")

    JWTManager(app)
