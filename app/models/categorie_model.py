from sqlalchemy import Column, Integer, String
from app.configs.database import db
from dataclasses import dataclass

@dataclass
class CategoriesModel(db.Model):
    id: int
    name: str

    __tablename__ = "categories"

    id: Column(Integer, primary_key=True)
    name: Column(String(80), nullable=False, unique=True)