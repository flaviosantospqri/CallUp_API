from sqlalchemy import Column, ForeignKey, String, Float, Integer
import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID
from dataclasses import dataclass
from werkzeug.exceptions import BadRequest
from sqlalchemy.orm import validates
from uuid import uuid4
from app.configs.database import db


@dataclass
class Proposal(db.Model):
    id: int
    price: float
    description: str

    __tablename__ = "proposals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    price = Column(Float(2), nullable=False)
    description = Column(String(255), nullable=False)
    call_id = Column(UUID(as_uuid=True), ForeignKey("calls.id"), nullable=False)
    provider_id = Column(UUID(as_uuid=True), ForeignKey("providers.id"), nullable=False)

    @validates("price")
    def verify_price(self, key, price_validate):
        if type(price_validate) != float:
            raise BadRequest(description={"error": "price must be a float"})
        return price_validate

    @validates("description")
    def verify_description(self, key, description_validate):
        if type(description_validate) != str:
            raise BadRequest(description={"error": "description must be a string"})

        return description_validate
