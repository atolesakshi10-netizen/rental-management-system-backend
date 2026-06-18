from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Property, Tenant, Agreement, Payment
from app.auth.dependencies import get_current_user

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("/stats")
def dashboard_stats(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return {
        "properties": db.query(Property).count(),
        "tenants": db.query(Tenant).count(),
        "agreements": db.query(Agreement).count(),
        "payments": db.query(Payment).count()
    }