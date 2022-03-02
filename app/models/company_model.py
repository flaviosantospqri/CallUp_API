from dataclasses import dataclass
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from app.configs.database import db
from sqlalchemy.orm import validates
from app.models.task_categories_model import task_categories
from app.exceptions.exc import InvalidDataError


@dataclass
class Categories(db.Model):
    id: Integer
    name: String
    cnpj: String
    email: String
    andress: String
    password: String

    __tablename__ = 'company'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)