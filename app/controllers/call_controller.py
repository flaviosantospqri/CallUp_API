from sqlite3 import IntegrityError
from app.models.call_model import Call
from app.models.employee_model import Employee
from flask import request, jsonify
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
from werkzeug.exceptions import Unauthorized, BadRequest

session: Session = db.session

@jwt_required()
def get_call():

    all_call = session.query(Call).all()

    return jsonify(all_call), HTTPStatus.OK

      
@jwt_required()
def get_call_id(id):
    try:
        current_user = get_jwt_identity()

        if current_user.type == "provider":
            raise Unauthorized

        employee = Employee.query.filter_by(id=id).first()
        calls_list = Call.query.filter_by(employee_id=employee.id)

        filtered_list = []

        for call in calls_list:
            if call.employee_id == employee.id:
                filtered_list.append(call)

        return jsonify(filtered_list), HTTPStatus.OK

    except Unauthorized:
        return {"error": "access denied"}, HTTPStatus.UNAUTHORIZED


@jwt_required
def post_call():
    try:
        current_user = get_jwt_identity()
        data = request.get_json()

        if current_user.type != "employee":
            raise Unauthorized

        default_keys = [
            "description",
            "open",
            "scheduling",
            "subcategory_id",
            "category_id",
            "employee_id",
        ]

        valid_data = {item: data[item] for item in data if item in default_keys}

        for key in default_keys:
            if key not in valid_data.keys():
                raise BadRequest(description={"error": f"Incomplete request, check {key} field"})

        valid_data["employee_id"] = current_user.id

        call = Call(**valid_data)

        session.add(call)
        session.commit()

    except IntegrityError:
        return {"error": "call already registred"}, HTTPStatus.CONFLICT

    except Unauthorized:
        return {"error": "access denied"}, HTTPStatus.UNAUTHORIZED
    
    except BadRequest as e:
        return e.description, HTTPStatus.BAD_REQUEST


      
@jwt_required()
def update_call(id):
    current_user = get_jwt_identity()

    if current_user.type != "employee":
        raise Unauthorized

    try:
        data = request.get_json()

        default_keys = ["description", "open", "scheduling", "subcategory_id", "category_id", "employee_id", "selected_proposal"]

        valid_data = {item: data[item] for item in data if item in default_keys}

        current_call = session.query(Call).get(id)

        for key, value in valid_data.items():
            setattr(current_call, key, value)

        session.add(current_call)
        session.commit()

        return jsonify(current_call), HTTPStatus.OK

    except NotFound:
        return {"msg": "call not found!"}, HTTPStatus.NOT_FOUND

    except Unauthorized:
        return {"error": "access denied"}, HTTPStatus.UNAUTHORIZED


@jwt_required()
def delete_call(id):
    current_user = get_jwt_identity()

    if current_user.type != "employee":
        raise Unauthorized

    try:        
        current_call = session.query(Call).get(id)

        session.delete(current_call)
        session.commit()

        return jsonify(current_call), HTTPStatus.OK

    except NotFound:
        return {"msg": "call not found!"}, HTTPStatus.NOT_FOUND
    
    except Unauthorized:
        return {"error": "access denied"}, HTTPStatus.UNAUTHORIZED