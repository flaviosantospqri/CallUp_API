from dataclasses import dataclass
import email
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import validates, relationship, backref
from werkzeug.security import check_password_hash, generate_password_hash
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from http import HTTPStatus
from app.configs.database import db
import re
from app.exc.provider_exc import CnpjFormatInvalidError, EmailFormatInvalidError, PasswordFormatinvalidError

@dataclass
class Company(db.Model):
    id: Integer
    name: String
    cnpj: String
    email: String
    address: String


    __tablename__ = "companies"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    cnpj = Column(String(18), nullable=False, unique=True)
    name = Column(String(127), nullable=False)
    address = Column(Text, nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(511), nullable=False)

    employees = relationship("Employee", backref=backref('company', uselist=False))

    @property
    def password(self):
        raise AttributeError("Password is not acessible")

    @password.setter
    def password(self, password_hash):
        self.password_hash = generate_password_hash(password_hash)


    def check_password(self, check_compare):
        return check_password_hash(self.password_hash, check_compare)




    @validates('email')
    def validate_email(self, key, email_for_validate):
        email_regex = re.compile(r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9]+.[a-zA-Z.a-zA-Z]{1,3}.?[a-zA-Z.a-zA-Z]{1,3}?$")
        validated_email = re.fullmatch(email_regex, email_for_validate)
        if not validated_email:
            raise EmailFormatInvalidError
        return email_for_validate

    @validates('password')
    def validate_password(self, key, password_to_validate):
        password_regex = re.compile(r"^(((?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%<^&*?])[a-zA-Z0-9!@#$%<^&*?]{8,})|([a-zA-Z]+([- .,_][a-zA-Z]+){4,}))$")
        validate_password = re.fullmatch(password_regex, password_to_validate)
        if not validate_password:
            raise PasswordFormatinvalidError
        return password_to_validate

    @validates('cnpj')       
    def validate_cnpj(self, key, cnpj_for_validate):
        cnpj_regex = re.compile(r"([0-9]{2}[.]?[0-9]{3}[.]?[0-9]{3}[\/]?[0-9]{4}[-]?[0-9]{2})")
        validate_cnpj = re.fullmatch(cnpj_regex, cnpj_for_validate)
        if not validate_cnpj:
            raise CnpjFormatInvalidError
        return cnpj_for_validate
    
    def check_fields(data):
        default_keys = ["name", "cnpj", "address", "email","password"]
        
        for key in default_keys:
            if key not in data.keys():
                return {"error": f"Incomplete request, check {key} field"}, HTTPStatus.BAD_REQUEST 
        for key in data.keys():
            if key not in default_keys:
                return {"error": f"Incomplete request, check {key} field"}, HTTPStatus.BAD_REQUEST
   

