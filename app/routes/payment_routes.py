from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import PaymentCreate
from app.auth.dependencies import get_current_user

from app.crud.payment_crud import (
    create_payment,
    get_payments,
    verify_payment_hash
)

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


@router.post("/")
def add_payment(
    payment_data: PaymentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    try:

        payment = create_payment(
            db,
            payment_data
        )

        return {
            "message": "Payment created successfully",
            "payment": payment
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get("/")
def view_payments(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return get_payments(db)


@router.get("/verify/{payment_id}")
def verify_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    result = verify_payment_hash(
        db,
        payment_id
    )

    if result is None:

        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    return result