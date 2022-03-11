from dataclasses import dataclass
import email
from sqlalchemy import Column, String, Text
from sqlalchemy.orm import validates, relationship, backref
from werkzeug.security import check_password_hash, generate_password_hash
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.exceptions import BadRequest
from app.configs.database import db
import re


@dataclass
class Company(db.Model):
    id: UUID
    name: str
    cnpj: str
    email: str
    address: str
    type: str

    __tablename__ = "companies"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    cnpj = Column(String(18), nullable=False, unique=True)
    name = Column(String(127), nullable=False)
    address = Column(Text, nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(511), nullable=False)
    type = Column(String, default="company")

    employees = relationship("Employee", backref=backref("company", uselist=False))

    @property
    def password(self):
        raise AttributeError("Password is not acessible")

    @password.setter
    def password(self, password_hash):

        password_regex = re.compile(
            r"^(((?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%<^&*?])[a-zA-Z0-9!@#$%<^&*?]{8,})|([a-zA-Z]+([- .,_][a-zA-Z]+){4,}))$"
        )
        validate_password = re.fullmatch(password_regex, password_hash)

        if not validate_password:
            raise BadRequest(description={"error": "Wrong password format"})

        self.password_hash = generate_password_hash(password_hash)

    def check_password(self, check_compare):
        return check_password_hash(self.password_hash, check_compare)

    @validates("name")
    def normalize_name(self, key, name_for_normalize):
        return name_for_normalize.title()

    @validates("email")
    def validate_email(self, key, email_for_validate):
        email_regex = re.compile(
            r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9]+.[a-zA-Z.a-zA-Z]{1,3}.?[a-zA-Z.a-zA-Z]{1,3}?$"
        )
        validated_email = re.fullmatch(email_regex, email_for_validate)

        if not validated_email:
            raise BadRequest(description={"error": "Wrong email format"})

        return email_for_validate.lower()

    @validates("cnpj")
    def validate_cnpj(self, _, cnpj_for_validate):
        cnpj_regex = re.compile(
            r"([0-9]{2}[.]?[0-9]{3}[.]?[0-9]{3}[\/]?[0-9]{4}[-]?[0-9]{2})"
        )
        validate_cnpj = re.fullmatch(cnpj_regex, cnpj_for_validate)

        if not validate_cnpj:
            raise BadRequest(description={"error": "Wrong CNPJ format"})

        return cnpj_for_validate

    @staticmethod
    def check_fields(data):
        default_keys = ["name", "cnpj", "address", "email", "password"]

        valid_data = {item: data[item] for item in data if item in default_keys}

        for key in default_keys:
            if key not in valid_data.keys():
                raise BadRequest(
                    description={"error": f"Incomplete request, check {key} field"}
                )

        return valid_data

    @staticmethod
    def check_data_for_update(data):
        update_fields = ["name", "address"]

        valid_data = {item: data[item] for item in data if item in update_fields}

        return valid_data
