from dataclasses import dataclass
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import validates, relationship, backref
from werkzeug.security import check_password_hash, generate_password_hash
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID

from app.configs.database import db


@dataclass
class Company(db.Model):
    id: Integer
    name: String
    cnpj: String
    email: String
    address: String
    password_hash: String
    
    __tablename__ = "companies"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(100), nullable=False, unique=True)
    cnpj = Column(String, nullable=False )
    address = Column(Text, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String(), nullable=False)

    employees = relationship("Employee", backref=backref('company', uselist=False))

    @property
    def password(self):
        raise AttributeError("Password is not acessible")

    @password.setter
    def password(self, password_hash):
        self.password_hash = generate_password_hash(password_hash)


    def check_password(self, check_compare):
        return check_password_hash(self.password_hash, check_compare)