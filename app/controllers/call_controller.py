from sqlite3 import IntegrityError
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


@jwt_required
def post_call():
    try:
        current_user = get_jwt_identity()
        data = request.get_json()

        if current_user.type != "employee":
            return {"error": "access denied"}, HTTPStatus.UNAUTHORIZED

        data["employee_id"] = current_user.id

        default_keys = [
            "description",
            "open",
            "scheduling",
            "subcategory_id",
            "category_id",
            "employee_id",
        ]

        for key in default_keys:
            if key not in data.keys():
                return {
                    "error": f"Incomplete request, check {key} field"
                }, HTTPStatus.BAD_REQUEST

        call = Call(**data)

        session.add(call)
        session.commit()
    except IntegrityError:
        return {"error": "call already registred"}, HTTPStatus.CONFLICT
