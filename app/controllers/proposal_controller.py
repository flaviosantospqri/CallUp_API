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