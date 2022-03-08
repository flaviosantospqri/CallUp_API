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

@jwt_required()
def get_call_id(id):
    current_user = get_jwt_identity()

    if current_user.type == "provider":
        return {"error": "access denied"}, HTTPStatus.UNAUTHORIZED

    employee = Employee.query.filter_by(id=id).first()
    calls_list = Call.query.filter_by(employee_id=employee.id)

    filtered_list = []

    for call in calls_list:
        if call.employee_id == employee.id:
            filtered_list.append(call)

    return jsonify(filtered_list), HTTPStatus.OK

@jwt_required()
def update_call(id):
    current_user = get_jwt_identity()

    if current_user.type != "employee":
        return {"error": "access denied"}, HTTPStatus.UNAUTHORIZED

    try:
        data = request.get_json()

        columns = ["description", "open", "scheduling", "subcategory_id", "category_id", "employee_id", "selected_proposal"]

        valid_data = {item: data[item] for item in data if item in columns}

        current_call = session.query(Call).get(id)

        for key, value in valid_data.items():
            setattr(current_call, key, value)

        session.add(current_call)
        session.commit()

        return jsonify(current_call), HTTPStatus.OK

    except NotFound:
        return {"msg": "call not found!"}, HTTPStatus.NOT_FOUND

