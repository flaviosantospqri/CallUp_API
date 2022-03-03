from sqlalchemy import Column, Integer, String
from app.configs.database import db
from dataclasses import dataclass

@dataclass
class SectorModel(db.Model):
    id: int
    name: str

    __tablename__ = "sectors"

    id: Column(Integer, primary_key=True)
    name: Column(String(225), nullable=False, unique=True)