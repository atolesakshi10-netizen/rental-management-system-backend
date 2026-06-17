from sqlalchemy.orm import Session

from app.models import Agreement
from app.schemas import AgreementCreate

from app.services.blockchain_service import (
    generate_agreement_hash
)


def create_agreement(
    db: Session,
    agreement_data: AgreementCreate
):

    agreement_hash = generate_agreement_hash(
        agreement_data.property_id,
        agreement_data.tenant_id,
        agreement_data.monthly_rent,
        agreement_data.start_date,
        agreement_data.end_date
    )

    new_agreement = Agreement(
        property_id=agreement_data.property_id,
        tenant_id=agreement_data.tenant_id,
        start_date=agreement_data.start_date,
        end_date=agreement_data.end_date,
        monthly_rent=agreement_data.monthly_rent,
        blockchain_hash=agreement_hash
    )

    db.add(new_agreement)
    db.commit()
    db.refresh(new_agreement)

    return new_agreement


def get_agreements(db: Session):

    return db.query(Agreement).all()


def verify_agreement_hash(
    db: Session,
    agreement_id: int
):

    agreement = db.query(Agreement).filter(
        Agreement.id == agreement_id
    ).first()

    if not agreement:
        return None

    current_hash = generate_agreement_hash(
        agreement.property_id,
        agreement.tenant_id,
        agreement.monthly_rent,
        agreement.start_date,
        agreement.end_date
    )

    if current_hash == agreement.blockchain_hash:
        return {
            "agreement_id": agreement_id,
            "status": "VALID"
        }

    return {
        "agreement_id": agreement_id,
        "status": "TAMPERED"
    }