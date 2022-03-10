from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, backref, validates
from app.configs.database import db
from dataclasses import dataclass
from uuid import uuid4
from http import HTTPStatus
import re
from app.exc.provider_exc import CnpjFormatInvalidError, EmailFormatInvalidError, PasswordFormatinvalidError

@dataclass
class Provider(db.Model):
    id: int
    name: str
    cnpj: str
    about: str
    email: str
    type: str

    __tablename__ = "providers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(127), nullable=False)
    cnpj = Column(String(18), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    about = Column(String(255))
    password_hash = Column(String(511), nullable=False)
    type = Column(String, default="provider")

    proposals = relationship("Proposal", backref=backref("provider", uselist=False))

    @property
    def password(self):
        raise AttributeError("Error password")

    @password.setter
    def password(self, password_to_hash):
        self.password_hash = generate_password_hash(password_to_hash)

    def password_check(self, password_to_compare):
        return check_password_hash(self.password_hash, password_to_compare)


    @validates("email")
    def validate_email(self, _, email_validate):
        email_regex = re.compile(r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9]+\.[a-zA-Z\.a-zA-Z]{1,3}\.?[a-zA-Z\.a-zA-Z]{1,3}?$")

        if not re.fullmatch(email_regex, email_validate):
            raise EmailFormatInvalidError
        return email_validate.lower()

    @validates("cnpj")
    def validate_cnpj(self, _, cnpj_validate):
        cnpj_regex = re.compile(r"([0-9]{2}[\.]?[0-9]{3}[\.]?[0-9]{3}[\/]?[0-9]{4}[-]?[0-9]{2})")

        if not re.fullmatch(cnpj_regex, cnpj_validate):
            raise CnpjFormatInvalidError
        return cnpj_validate


    @validates('name')
    def normalize_name(self, _, name_normalize):
        return name_normalize.title()
        
    @validates('password')
    def validate_password(self, _, password_validate):
        password_regex = re.compile(r"([0-9]{2}[\.]?[0-9]{3}[\.]?[0-9]{3}[\/]?[0-9]{4}[-]?[0-9]{2})")
        if not re.fullmatch(password_regex, password_validate):
            raise PasswordFormatinvalidError
        return password_validate

    def check_fields(data):
        default_keys = ["name", "cnpj", "email","password"]

        for key in default_keys:
            if key not in data.keys():
                return {"error": f"Incomplete request, check {key} field"}, HTTPStatus.BAD_REQUEST
        for key in data.keys():
            if key not in default_keys:
                return {"error": f"Incomplete request, check {key} field"}, HTTPStatus.BAD_REQUEST

    def check_data_update(data):
        update_fields = ["name", "about"]
        valid_data = {item: data[item] for item in data if item in update_fields}

        for key, value in valid_data.items():
            setattr(data, key, value)
        return data