from sqlalchemy import Column, ForeignKey, String, Float, Integer
from sqlalchemy.dialects.postgresql import UUID
from dataclasses import dataclass

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
    call_id = Column(UUID(as_uuid=True), ForeignKey('calls.id'), nullable=False)
    provider_id = Column(UUID(as_uuid=True), ForeignKey('providers.id'), nullable=False)

