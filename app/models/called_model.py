from sqlalchemy import Column, Integer, Boolean, Date, String
from sqlalchemy.dialects.postgresql import UUID
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
    scheduling: Column(Date)