from dataclasses import dataclass

from sqlalchemy import Column, Integer, ForeignKey

from app.configs.database import db


@dataclass
class Provider_customer(db.Model):
    id: int
    provider_id: int
    customer_id: int

    __tablename__ = "provider_customer"


    id = Column(Integer, primary_key=True)
    provider_id = Column(Integer, ForeignKey('provider.id'), nullable=False)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
