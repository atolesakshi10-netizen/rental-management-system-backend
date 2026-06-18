from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import BlockchainRecord
from app.auth import get_current_user

router = APIRouter(
    prefix="/blockchain",
    tags=["Blockchain"]
)

@router.get("/")
def get_blockchain(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    records = db.query(BlockchainRecord).all()
    return records