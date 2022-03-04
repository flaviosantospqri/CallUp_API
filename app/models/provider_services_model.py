from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer
from app.configs.database import db
from dataclasses import dataclass
from  uuid import uuid4

@dataclass
class Provider(db.Model):
    id: int
    name: str
    cnpj: str
    about: str
    email: str
    password_hash: str

    __tablename__ = 'providers'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(127), nullable=False)
    cnpj = Column(String(511), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    about = Column(String(255))
    password_hash = Column(String(511), nullable=False)

    @property
    def password(self):
        raise AttributeError("Error password")
    
    @password.setter
    def password(self, password_to_hash):
        self.password_hash = generate_password_hash(password_to_hash)
    
    def password_check(self, password_to_compare):
        return check_password_hash(self.password_hash, password_to_compare)

