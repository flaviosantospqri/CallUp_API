from flask import Flask
from flask_jwt_extended import JWTManager
from os import getenv


def init_app(app: Flask):
    app.config["JWT_SECRET_KEY"] = getenv("SECRET")

    JWTManager(app)
