from sqlalchemy.orm import relationship, backref, validates
from sqlalchemy import Column, String, ForeignKey
from werkzeug.security import check_password_hash, generate_password_hash
from app.configs.database import db
from dataclasses import dataclass
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
import re
from werkzeug.exceptions import BadRequest
from app.exc.provider_exc import EmailFormatInvalidError, PhoneFormatInvalidError



@dataclass
class Employee(db.Model):
    id: int
    name: str
    company_id: int
    sector_id: int
    phone: str
    email: str
    type: str

    __tablename__ = "employees"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(127), nullable=False, unique=True)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"))
    sector_id = Column(UUID(as_uuid=True), ForeignKey("sectors.id"))
    phone = Column(String(255))
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(511), nullable=False)
    type = Column(String, default="employee")

    calls = relationship("Call", backref=backref("employee", uselist=False))
    providers = relationship(
        "Provider", secondary="providers_customers", backref="clients"
    )

    @property
    def password(self):
        raise AttributeError("Password is not acessible")

    @password.setter
    def password(self, password_hash):
      
        password_regex = re.compile(
        r"^(((?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%<^&*?])[a-zA-Z0-9!@#$%<^&*?]{8,})|([a-zA-Z]+([- .,_][a-zA-Z]+){4,}))$"
        )
        validate_password = re.fullmatch(password_regex, data["password"])
        
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
            raise BadRequest(description={"error": "this no a valid e-mail"})
        return email_for_validate.lower()

    @validates("phone")
    def validate_phone(self, key, phone_for_validate):
        phone_regex = re.compile(
            r"^(([1-9]{2})[9]{1}[0-9]{4}-[0-9]{4})|(([1-9]{2})[1-9]{1}[0-9]{3}-[0-9]{4})$"
        )
        validated_phone = re.fullmatch(phone_regex, phone_for_validate)
        if not validated_phone:
            raise BadRequest(description={"error": "this no a valid phone number"})
        return phone_for_validate
