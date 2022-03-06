from flask import request, jsonify, session
from http import HTTPStatus


from app.configs.database import db
from sqlalchemy.orm.session import Session

from sqlalchemy.exc import IntegrityError

session: Session = db.session

def get_employees(id):
    ...
def post_employee(id):
    ...
def patch_employee(id):
    ...
def delete_employee(id):
    ...
def find_employees(id):
    ... 