from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import AuditLog
from app.auth.dependencies import get_current_user

router = APIRouter(
    prefix="/audit",
    tags=["Audit Logs"]
)

@router.get("/")
def view_audit_logs(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    logs = (
        db.query(AuditLog)
        .order_by(AuditLog.timestamp.desc())
        .all()
    )

    return logs