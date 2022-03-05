from sqlalchemy import Column, Integer, Boolean, Date, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref
from uuid import uuid4

from app.configs.database import db
from dataclasses import dataclass

@dataclass
class Call(db.Model):
    id: int
    description: str
    open: bool
    scheduling: str

    __tablename__ = "calls"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    description = Column(String(225))
    open = Column(Boolean)
    scheduling= Column(Date)
    category_id = Column(UUID(as_uuid=True), ForeignKey('categories.id'), nullable=False)
    subcategory_id = Column(UUID(as_uuid=True), ForeignKey('subcategories.id'), nullable=False)
    employee_id = Column(UUID(as_uuid=True), ForeignKey('employees.id'), nullable=False)
    selected_proposal = Column(UUID(as_uuid=True), ForeignKey('proposals.id'), nullable=False)

    proposals = relationship("Proposal", backref=backref('call', uselist=False))
    providers = relationship("Provider", secondary='proposals', backref='calls')