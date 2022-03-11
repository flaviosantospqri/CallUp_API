from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, backref
from uuid import uuid4

from app.configs.database import db
from dataclasses import dataclass


@dataclass
class Sector(db.Model):
    name: str

    __tablename__ = "sectors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(127), nullable=False, unique=True)

    
