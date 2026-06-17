from sqlalchemy.orm import Session

from app.schemas import PaymentCreate
from app.models import Payment, Agreement, Tenant

from app.services.email_service import send_email
from app.services.blockchain_service import generate_payment_hash


def create_payment(
    db: Session,
    payment_data: PaymentCreate
):

    payment_hash = generate_payment_hash(
        payment_data.agreement_id,
        payment_data.amount,
        payment_data.payment_date,
        payment_data.payment_status
    )

    new_payment = Payment(
        agreement_id=payment_data.agreement_id,
        amount=payment_data.amount,
        payment_date=payment_data.payment_date,
        payment_status=payment_data.payment_status,
        blockchain_hash=payment_hash
    )

    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)

    agreement = db.query(
        Agreement
    ).filter(
        Agreement.id == payment_data.agreement_id
    ).first()

    if agreement is None:
        raise Exception("Agreement not found")

    tenant = db.query(
        Tenant
    ).filter(
        Tenant.id == agreement.tenant_id
    ).first()

    if tenant is None:
        raise Exception("Tenant not found")

    if not tenant.email:
        raise Exception("Tenant email is empty")

    body = f"""
Payment Received Successfully

Amount: ₹{payment_data.amount}

Date: {payment_data.payment_date}

Status: {payment_data.payment_status}

Agreement ID: {payment_data.agreement_id}

Thank You.
"""

    send_email(
        tenant.email,
        "Payment Receipt",
        body
    )

    return new_payment


def get_payments(db: Session):

    return db.query(Payment).all()


def verify_payment_hash(
    db: Session,
    payment_id: int
):

    payment = db.query(
        Payment
    ).filter(
        Payment.id == payment_id
    ).first()

    if payment is None:
        return None

    current_hash = generate_payment_hash(
        payment.agreement_id,
        payment.amount,
        payment.payment_date,
        payment.payment_status
    )

    if current_hash == payment.blockchain_hash:

        return {
            "payment_id": payment_id,
            "status": "VALID"
        }

    return {
        "payment_id": payment_id,
        "status": "TAMPERED"
    }