from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String
from uuid import uuid4

from app.configs.database import db
from dataclasses import dataclass

@dataclass
class SubCategory(db.Model):
    id: int
    name: str

    __tablename__ = "subcategories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(80), nullable=False, unique=True)