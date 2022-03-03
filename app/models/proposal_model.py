from sqlalchemy import Column, ForeignKey, Integer, String, Float
from dataclasses import dataclass

from app.configs.database import db

@dataclass
class Proposal(db.Model):
    id: int
    price: float
    description: str

    __tablename__ = "proposals"


    id = Column(Integer, primary_key=True)
    price = Column(Float(2), nullable=False)
    description = Column(String(255), nullable=False)
    call_id = Column(Integer, ForeignKey('calls.id'))
    provider_id = Column(Integer, ForeignKey('providers.id'))