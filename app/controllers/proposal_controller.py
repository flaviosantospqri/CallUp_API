from app.models.employee_model import Employee
from app.models.proposal_model import Proposal
from flask import request, jsonify, current_app
import re
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError
from app.configs.database import db
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import UnmappedInstanceError
from flask_jwt_extended import (create_access_token, get_jwt_identity, jwt_required)

session : Session = db.session

def get_proposals():
    proposals = session.query(Employee).all()

    if not proposals:
        return jsonify({"Proposals": []})
    return jsonify(proposals), HTTPStatus.OK

def get_proposal_accepted():
    current_user = get_jwt_identity

    if current_user.type != "provider":
        return {"error": "acess denied"}, HTTPStatus.UNAUTHORIZED
    
    ...
@jwt_required()
def create_proposal():
    
    current_user = get_jwt_identity()
    # if current_user.type != "provider":
    #     return {"error": "access denied"}, HTTPStatus.BAD_REQUEST
    
    data = request.get_json()
    data["provider_id"] = current_user
    
    default_keys = ["price", "description", "provider_id", "call_id"]

    for key in default_keys:
        if key not in data.keys():
            return {
                "error": f"Incomplete request, check {key} field"
            }, HTTPStatus.BAD_REQUEST

    for key in data.keys():
        if key not in default_keys:
            return {
                "error": f"Incomplete request, check {key} field"
            }, HTTPStatus.BAD_REQUEST

    try:
        proposal = Proposal(**data)

        session.add(proposal)
        session.commit()
    except IntegrityError:
        return {"error": "Proposal already registred"}, HTTPStatus.CONFLICT
    
    return jsonify(proposal), HTTPStatus.CREATED

