from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from werkzeug.exceptions import NotFound, Unauthorized, BadRequest
from sqlalchemy.orm.exc import UnmappedInstanceError
from flask import request, jsonify
from app.models.call_model import Call
from app.models.proposal_model import Proposal
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError
from app.configs.database import db
from http import HTTPStatus

from app.models.provider_model import Provider


session: Session = db.session


def get_proposals():
    proposals = session.query(Proposal).all()

    return jsonify(proposals), HTTPStatus.OK


@jwt_required()
def get_accepted_proposals():
    try:
        current_user = get_jwt_identity()

        if current_user["type"] != "provider":
            raise Unauthorized

        call_list = Call.query.all()

        final_list = []

        for call in call_list:
            if (
                call.selected_proposal != None
                and call.selected_proposal.provider_id == current_user["id"]
            ):
                final_list.append({"call": call, "proposal": call.selected_proposal})
        return jsonify(final_list), HTTPStatus.OK

    except BadRequest as e:
        return e.description, HTTPStatus.BAD_REQUEST

    except Unauthorized:
        return {"error": "access denied"}, HTTPStatus.BAD_REQUEST


@jwt_required()
def create_proposal():
    current_user = get_jwt_identity()
    try:
        if current_user["type"] != "provider":
            raise Unauthorized

        data = request.get_json()

        provider_id = current_user["id"]
        call_id = data.pop("call_id")

        provider: Provider = session.query(Provider).get_or_404(
            provider_id, description={"error": "provider doesn't exist"}
        )

        call: Call = session.query(Call).get_or_404(
            call_id, description={"error": "call doesn't exist"}
        )

        valid_data = Proposal.check_fields(data)

        proposal = Proposal(**valid_data)

        provider.proposals.append(proposal)
        call.proposals.append(proposal)

        session.add(proposal)
        session.commit()

        return jsonify(proposal), HTTPStatus.CREATED

    except BadRequest as e:
        return e.description, HTTPStatus.BAD_REQUEST

    except IntegrityError:
        return {"error": "Proposal already registred"}, HTTPStatus.CONFLICT

    except Unauthorized:
        return {"error": "access denied"}, HTTPStatus.BAD_REQUEST


@jwt_required()
def update_proposal(proposal_id):

    current_user = get_jwt_identity()

    try:

        if current_user["type"] != "provider":
            raise Unauthorized

        data = request.get_json()

        proposal: Proposal = Proposal.query.get_or_404(proposal_id)

        if proposal.provider_id != current_user["id"]:
            raise Unauthorized

        valid_data = Proposal.check_data_for_update(data)

        for key, value in valid_data.items():
            setattr(proposal, key, value)

        session.add(proposal)
        session.commit()

        return jsonify(proposal), HTTPStatus.OK

    except BadRequest as e:
        return e.description, HTTPStatus.BAD_REQUEST

    except NotFound:
        return {"error": f"Proposal {proposal_id} do not found"}, HTTPStatus.NOT_FOUND

    except Unauthorized:
        return {"error": "access denied"}, HTTPStatus.BAD_REQUEST


@jwt_required()
def delete_proposal(proposal_id):
    current_user = get_jwt_identity()

    try:

        proposal: Proposal = Proposal.query.get_or_404(proposal_id)

        if proposal.provider_id != current_user["id"]:
            raise Unauthorized

        session.delete(proposal)
        session.commit()

        return "", HTTPStatus.OK
    except BadRequest as e:
        return e.description, HTTPStatus.BAD_REQUEST

    except NotFound:
        return {"error": f"Proposal {proposal_id} do not found"}, HTTPStatus.NOT_FOUND
