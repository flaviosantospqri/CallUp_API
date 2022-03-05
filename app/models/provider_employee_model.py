from dataclasses import dataclass

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, ForeignKey

from uuid import uuid4

from app.configs.database import db


@dataclass
class ProviderEmployee(db.Model):
    id: int
    provider_id: int
    employee_id: int

    __tablename__ = "providers_customers"


    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    provider_id = Column(UUID(as_uuid=True), ForeignKey('providers.id'), nullable=False)
    employee_id = Column(UUID(as_uuid=True), ForeignKey('employees.id'), nullable=False)
