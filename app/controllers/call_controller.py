from app.models.call_model import Call
from app.models.employee_model import Employee
from flask import request, jsonify, session
from http import HTTPStatus
from werkzeug.exceptions import NotFound
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    jwt_required,
    get_jwt_identity,
)
from app.configs.database import db
from sqlalchemy.orm.session import Session
import re

session: Session = db.session


def get_call():
    try:
        all_call = session.query(Call).all()

        if all_call:
            return jsonify(all_call), HTTPStatus.OK
    except NotFound:
        return jsonify(all_call), HTTPStatus.NOT_FOUND
