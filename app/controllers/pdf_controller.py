from flask import current_app, render_template
from flask_mail import Message, Mail
from pdfkit import from_string
from os import getenv
from app.models.company_model import Company
from app.models.employee_model import Employee
from app.models.call_model import Call
from flask_jwt_extended import get_jwt_identity, jwt_required

@jwt_required()
def send_pdf():
    mail: Mail = current_app.mail

    current_user = get_jwt_identity()

    company = Company.query.filter_by(email=current_user.email).first()
    employees = Employee.query.filter_by(company_id=company.id).all()
    calls = Call.query.all()

    company_calls = []

    for call in calls:
        for employee in employees:
            if call.employee_id == employee.id:
                company_calls.append(call)


    pdf = from_string(render_template("pdf/template.html", name=company.name, calls=company_calls), False)

    msg = Message(
        subject="Report",
        sender=getenv("MAIL_USERNAME"),
        recipients=[company.email],
        html=render_template("email/template.html")
    )

    msg.attach("report.pdf", "application/pdf", pdf)

    mail.send(msg)

    return {"stts": "ok"}, 200
