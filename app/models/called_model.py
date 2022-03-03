from sqlalchemy import Column, Integer, Boolean, Date, String
from app.configs.database import db
from dataclasses import dataclass

@dataclass
class CalledModel(db.Model):
    id: int
    description: str
    open: bool
    scheduling: str

    __tablename__ = "calls"

    id: Column(Integer, primary_key=True)
    description: Column(String(225))
    open: Column(Boolean)
    scheduling: Column(Date)