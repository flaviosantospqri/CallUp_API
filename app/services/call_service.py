from app.models.employee_model import Employee
from app.models.provider_model import Provider
from sqlalchemy.orm.session import Session
from app.configs.database import db


session: Session = db.session


def relate_employee_provider(proposal, employee_id):
    employee: Employee = session.query(Employee).get_or_404(
        employee_id, description={"error": "employee not found"}
    )

    provider: Provider = session.query(Provider).get_or_404(
        proposal.provider_id, description={"error": "provider not found"}
    )

    employee.providers.append(provider)
    session.add(employee)
