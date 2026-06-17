from sqlalchemy.orm import Session

from app.models import (
    Property,
    Tenant,
    Agreement,
    Payment
)


def get_dashboard_data(db: Session):

    total_properties = db.query(Property).count()

    total_tenants = db.query(Tenant).count()

    total_agreements = db.query(Agreement).count()

    payments = db.query(Payment).all()

    total_revenue = sum(
        payment.amount
        for payment in payments
    )

    return {
        "total_properties": total_properties,
        "total_tenants": total_tenants,
        "total_agreements": total_agreements,
        "total_revenue": total_revenue
    }