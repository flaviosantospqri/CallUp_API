from app.configs import database, migrations, jwt_auth, email
from flask import Flask
from app import routes


def create_app():
    app = Flask(__name__)

    app.config["JSON_SORT_KEY"] = False

    email.init_app(app)
    database.init_app(app)
    migrations.init_app(app)
    jwt_auth.init_app(app)
    routes.init_app(app)

    return app
