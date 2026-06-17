from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import AgreementCreate
from app.auth.dependencies import get_current_user

from app.crud.agreement_crud import (
    create_agreement,
    get_agreements,
    verify_agreement_hash
)

router = APIRouter(
    prefix="/agreements",
    tags=["Agreements"]
)


@router.post("/")
def add_agreement(
    agreement_data: AgreementCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return create_agreement(
        db,
        agreement_data
    )


@router.get("/")
def view_agreements(
    db: Session = Depends(get_db)
):
    return get_agreements(db)


@router.get("/verify/{agreement_id}")
def verify_agreement(
    agreement_id: int,
    db: Session = Depends(get_db)
):

    result = verify_agreement_hash(
        db,
        agreement_id
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Agreement not found"
        )

    return result