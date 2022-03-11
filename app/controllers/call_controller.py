from sqlalchemy.exc import IntegrityError
from app.models.call_model import Call
from app.models.category_model import Category
from app.models.employee_model import Employee
from app.models.proposal_model import Proposal
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

from app.services.call_service import relate_employee_provider

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


@jwt_required()
def post_call():
    try:
        current_user = get_jwt_identity()
        data = request.get_json()

        if current_user["type"] != "employee":
            raise Unauthorized

        valid_data = Call.check_fields(data)

        category_name = valid_data.pop("category")
        subcategory_name = valid_data.pop("subcategory")

        category: Category = (
            session.query(Category)
            .filter_by(name=category_name)
            .first_or_404(description={"error": "category doesn't exist"})
        )

        subcategory: SubCategory = (
            session.query(SubCategory)
            .filter_by(name=subcategory_name)
            .first_or_404(description={"error": "subcategory doesn't exist"})
        )

        employee = session.query(Employee).filter_by(id=current_user["id"]).first()

        call = Call(**valid_data)

        category.calls.append(call)
        subcategory.calls.append(call)
        employee.calls.append(call)

        session.add(call)
        session.commit()

        return jsonify(call), HTTPStatus.CREATED

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

    try:

        if current_user["type"] != "employee":
            raise Unauthorized

        valid_data = Call.check_data_for_update(data)

        current_call = Call.query.filter_by(id=id).first_or_404(
            description={"error": "call doesn't exist"}
        )

        if str(current_call.employee_id) != current_user["id"]:
            raise Unauthorized

        if "category" in data:
            category_name = data.pop("categories")
            current_call.category_id = None

            category = (
                session.query(Category)
                .filter_by(name=category_name)
                .first_or_404(description={"error": "category doesn't exist"})
            )

            category.calls.append(current_call)

        if "subcategory" in data:
            subcategory_name = data.pop("subcategory")
            current_call.subcategory_id = None

            subcategory = (
                session.query(SubCategory)
                .filter_by(name=subcategory_name)
                .first_or_404(description={"error": "subcategory doesn't exist"})
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

    try:
        if current_user["type"] != "employee":
            raise Unauthorized

        current_call = session.query(Call).get_or_404(id)

        if str(current_call.employee_id) != current_user["id"]:
            raise Unauthorized

        session.delete(current_call)
        session.commit()

        return jsonify(current_call), HTTPStatus.OK

    except NotFound:
        return {"msg": "call not found!"}, HTTPStatus.NOT_FOUND

    except Unauthorized:
        return {"error": "access denied"}, HTTPStatus.UNAUTHORIZED


@jwt_required()
def close_call(call_id):
    current_user = get_jwt_identity()

    data = request.get_json()

    try:
        if current_user["type"] != "employee":
            raise Unauthorized(description={"error": "access denied"})

        current_call: Call = session.query(Call).get_or_404(
            call_id, description={"error": "proposal not found"}
        )

        if current_call.open == False:
            raise Unauthorized(description={"error": "call already closed"})

        if str(current_call.employee_id) != current_user["id"]:
            raise Unauthorized(description={"error": "access denied"})

        proposal_id = data.pop("selected_proposal_id")

        proposal: Proposal = session.query(Proposal).get_or_404(
            proposal_id, description={"error": "proposal not found"}
        )

        if str(proposal.call_id) != call_id:
            raise BadRequest

        current_call.open = False
        current_call.selected_proposal_id = proposal_id

        relate_employee_provider(proposal, current_user["id"])

        session.add(current_call)
        session.commit()

        return current_call, HTTPStatus.OK

    except KeyError:
        return {
            "error": "Incomplete request, check selected_proposal_id field"
        }, HTTPStatus.BAD_REQUEST

    except NotFound as e:
        return e.description, HTTPStatus.NOT_FOUND

    except Unauthorized as e:
        return e.description, HTTPStatus.UNAUTHORIZED

    except BadRequest:
        return {
            "error": "selected proposal doesn't belong to call"
        }, HTTPStatus.BAD_REQUEST
