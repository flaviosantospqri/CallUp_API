from flask import request, jsonify, current_app, render_template
from app.models.company_model import Company
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError
from app.configs.database import db
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import UnmappedInstanceError
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from werkzeug.exceptions import BadRequest, Unauthorized, NotFound
from flask_mail import Message, Mail
from pdfkit import from_string
from os import getenv

session: Session = db.session


@jwt_required()
def get_company():

    current_company = get_jwt_identity()
    print(current_company)

    company = session.query(Company).get(current_company["id"])
    print()

    return {
        "id": company.id,
        "name": company.name,
        "cnpj": company.cnpj,
        "address": company.address,
        "email": company.email,
        "employees": company.employees
    }, HTTPStatus.OK



def post_company():
    data = request.get_json()

    valid_data = Company.check_fields(data)

    try:
        company = Company(**valid_data)

        session.add(company)
        session.commit()

        return jsonify(company), HTTPStatus.CREATED

    except IntegrityError:
        return {"error": "company already registred"}, HTTPStatus.CONFLICT

    except BadRequest as e:
        return e.description, HTTPStatus.BAD_REQUEST


@jwt_required()
def update_company():
    try:
        data = request.get_json()
        current_user = get_jwt_identity()

        if current_user["type"] != "company":
            raise Unauthorized

        company = session.query(Company).get_or_404(current_user["id"])

        valid_data = Company.check_data_for_update(data)

        for key, value in valid_data.items():
            setattr(company, key, value)

        session.add(company)
        session.commit()

        return jsonify(company), HTTPStatus.OK

    except NotFound:
        return {"error": "company not found!"}, HTTPStatus.NOT_FOUND

    except Unauthorized:
        return {"error": "access denied"}, HTTPStatus.BAD_REQUEST

    

@jwt_required()
def delete_company():
    try:
        current_user = get_jwt_identity()

        company = session.query(Company).get(current_user["id"])

        session.delete(company)
        session.commit()

        return "", HTTPStatus.OK

    except UnmappedInstanceError:
        return {"error": "company not found!"}, HTTPStatus.NOT_FOUND


def signin_company():
    data = request.get_json()

    try:
        company: Company = Company.query.filter_by(email=data["email"]).first()

        if not company or not company.check_password(data["password"]):
            raise Unauthorized

        token = create_access_token(company)

        return {"token": token}, HTTPStatus.OK
    
    except Unauthorized:
        return {"error": "E-mail and/or password incorrect."}, HTTPStatus.UNAUTHORIZED

@jwt_required()
def send_pdf():
    try:
        mail: Mail = current_app.mail

        current_user = get_jwt_identity()

        if current_user["type"] != "company":
            raise Unauthorized


        company = Company.query.filter_by(email=current_user.email).first()

        company_calls = [call for employee in company["employees"] for call in employee["calls"]]


        pdf = from_string(
            render_template("pdf/template.html", name=company.name, calls=company_calls),
            False,
        )

        msg = Message(
            subject="Report",
            sender=getenv("MAIL_USERNAME"),
            recipients=[company.email],
            html=render_template("email/template.html"),
        )

        msg.attach("report.pdf", "application/pdf", pdf)

        mail.send(msg)

        return {"stts": "ok"}, HTTPStatus.OK
    
    except Unauthorized:
        return {"error": "access denied"}, HTTPStatus.BAD_REQUEST
