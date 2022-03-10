from http import HTTPStatus
from sqlalchemy import Column, Boolean, Date, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref, validates
from uuid import uuid4
from werkzeug.exceptions import BadRequest
from typing import Union

from app.configs.database import db
from app.models.proposal_model import Proposal
from dataclasses import dataclass

from datetime import datetime


@dataclass
class Call(db.Model):
    id: UUID
    description: str
    open: bool
    scheduling: str
    selected_proposal: Union[Proposal, None]

    __tablename__ = "calls"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    description = Column(String(225))
    open = Column(Boolean, default=True)
    scheduling = Column(Date)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"))
    subcategory_id = Column(UUID(as_uuid=True), ForeignKey("subcategories.id"))
    employee_id = Column(UUID(as_uuid=True), ForeignKey("employees.id"))
    selected_proposal_id = Column(UUID(as_uuid=True), ForeignKey("proposals.id"))

    proposals = relationship(
        "Proposal",
        backref=backref("call", uselist=False),
        foreign_keys="Proposal.call_id",
    )

    @property
    def selected_proposal(self):

        proposal = Proposal.query.filter_by(id=self.selected_proposal_id).first()

        if proposal:
            return proposal

        return None

    @validates("description")
    def verify_description(self, key, description):
        if type(description) != str:
            raise BadRequest({"error": "description must be a string"})

        return description

    @validates("scheduling")
    def verify_scheduling(self, key, description):
        try:
            return datetime.strptime(description, "%d/%m/%Y %H:%M")
        except:
            raise BadRequest(
                {
                    "error": "This is the incorrect date string format. It should be 'DD/MM/YYYY hh:mm' "
                }
            )

    @validates("open")
    def verify_open(self, key, open):
        if type(open) != bool:
            raise BadRequest({"error": "open must be a boolean"})

        return open

    @staticmethod
    def check_fields(data):

        default_keys = [
            "description",
            "subcategory",
            "category",
        ]

        valid_data = {item: data[item] for item in data if item in default_keys}

        for key in default_keys:
            if key not in valid_data.keys():
                return {
                    "error": f"Incomplete request, check {key} field"
                }, HTTPStatus.BAD_REQUEST

        return valid_data

    @staticmethod
    def check_data_for_update(data):
        update_fields = [
            "description",
            "open",
            "scheduling",
            "subcategory",
            "category",
            "selected_proposal_id",
        ]

        valid_data = {item: data[item] for item in data if item in update_fields}

        return valid_data
