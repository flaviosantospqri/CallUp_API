from sqlite3 import IntegrityError
from app.models.call_model import Call
from app.models.category_model import Category
from app.models.employee_model import Employee
from app.models.subcategory_model import SubCategory
from flask import request, jsonify
from http import HTTPStatus
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    jwt_required,
    get_jwt_identity,
)
from app.configs.database import db
from sqlalchemy.orm.session import Session
from werkzeug.exceptions import Unauthorized, BadRequest, NotFound

session: Session = db.session


@jwt_required()
def get_call():

    all_call = session.query(Call).all()

    return jsonify(all_call), HTTPStatus.OK


@jwt_required()
def get_call_id(id):
    try:
        current_user = get_jwt_identity()

        if current_user["type"] == "provider":
            raise Unauthorized

        employee = Employee.query.filter_by(id=id).first_or_404()

        return jsonify(employee.calls), HTTPStatus.OK

    except Unauthorized:
        return {"error": "access denied"}, HTTPStatus.UNAUTHORIZED

    except NotFound:
        return {"msg": "call not found!"}, HTTPStatus.NOT_FOUND

    except BadRequest as e:
        return e.description, HTTPStatus.BAD_REQUEST


@jwt_required
def post_call():
    try:
        current_user = get_jwt_identity()
        data = request.get_json()

        if current_user["type"] != "employee":
            raise Unauthorized

        valid_data = Call.check_fields(data)

        category_name = data.pop("category")
        subcategory_name = data.pop("subcategory")

        category = (
            session.query(Category)
            .filter_by(name=category_name)
            .first_or_404(description={"error": "category doesn't exist"})
        )

        subcategory = (
            session.query(SubCategory)
            .filter_by(name=subcategory_name)
            .first_or_404(description={"error": "subcategory doesn't exist"})
        )

        employee = session.query(Employee).filter_by(id=current_user["id"]).first()

        call = Call(**valid_data)

        category.append(call)
        subcategory.append(call)
        employee.append(call)

        session.add(call)
        session.commit()

    except IntegrityError:
        return {"error": "call already registred"}, HTTPStatus.CONFLICT

    except Unauthorized:
        return {"error": "access denied"}, HTTPStatus.UNAUTHORIZED

    except NotFound as e:
        e.description, HTTPStatus.NOT_FOUND


@jwt_required()
def update_call(id):
    current_user = get_jwt_identity()

    data = request.get_json()

    if current_user["type"] != "employee":
        raise Unauthorized

    try:

        valid_data = Call.check_data_for_update(data)

        current_call = Call.query.filter_by(id=id).first_or_404(
            description={"error": "call doesn't exist"}
        )

        if "category" in data:
            category_name = data.pop("categories")
            current_call.category_id = None

            category = (
                session.query(Category)
                .filter_by(name=category_name)
                .first_or_404(description={"error": "category doesn't exist"})
            )

            category.append(current_call)

        if "subcategory" in data:
            subcategory_name = data.pop("subcategory")
            current_call.subcategory_id = None

            subcategory = (
                session.query(SubCategory)
                .filter_by(name=subcategory_name)
                .first_or_404(description={"error": "category doesn't exist"})
            )

            subcategory.calls.append(current_call)

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

    if current_user["type"] != "employee":
        raise Unauthorized

    try:
        current_call = session.query(Call).get_or_404(id)

        session.delete(current_call)
        session.commit()

        return jsonify(current_call), HTTPStatus.OK

    except NotFound:
        return {"msg": "call not found!"}, HTTPStatus.NOT_FOUND

    except Unauthorized:
        return {"error": "access denied"}, HTTPStatus.UNAUTHORIZED
