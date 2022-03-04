from sqlalchemy import Column, Integer, String, ForeignKey
from werkzeug.security import check_password_hash, generate_password_hash
from app.configs.database import db
from dataclasses import dataclass
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

@dataclass
class Employees(db.Model):
    id: int
    name: str
    company_id: int
    sector_id: int
    phone: str
    email: str

    __tablename__ = "employees"

    id: Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Column(String(80), nullable=False, unique=True)
    company_id: Column(Integer, ForeignKey('companies.id'), nullable=False)
    sector_id: Column(Integer, ForeignKey('sectors.id'), nullable=False)
    phone: Column(String(255))
    email: Column(String(255), unique=True, nullable=False)
    password_hash: Column(String)

    @property
    def password(self):
        raise AttributeError("Password is not acessible")

    @password.setter
    def password(self, password_hash):
        self.password_hash = generate_password_hash(password_hash)


    def check_password(self, check_compare):
        return check_password_hash(self.password_hash, check_compare)