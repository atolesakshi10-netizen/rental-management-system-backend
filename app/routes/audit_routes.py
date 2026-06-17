from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import AuditLog
from app.auth.rbac import admin_required

router = APIRouter(
    prefix="/audit-logs",
    tags=["Audit Logs"]
)


@router.get("/")
def view_audit_logs(
    db: Session = Depends(get_db),
    current_user = Depends(admin_required)
):

    logs = db.query(AuditLog).all()

    return logs