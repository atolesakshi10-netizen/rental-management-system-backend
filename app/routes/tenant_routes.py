from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import TenantCreate
from app.auth.dependencies import get_current_user

from app.crud.tenant_crud import (
    create_tenant,
    get_tenants,
    update_tenant,
    delete_tenant
)

router = APIRouter(
    prefix="/tenants",
    tags=["Tenants"]
)


# CREATE TENANT (Protected)
@router.post("/")
def add_tenant(
    tenant_data: TenantCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return create_tenant(
        db,
        tenant_data
    )


# GET ALL TENANTS (Public)
@router.get("/")
def view_tenants(
    db: Session = Depends(get_db)
):
    return get_tenants(db)


# UPDATE TENANT (Protected)
@router.put("/{tenant_id}")
def edit_tenant(
    tenant_id: int,
    tenant_data: TenantCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):

    updated_tenant = update_tenant(
        db,
        tenant_id,
        tenant_data
    )

    if not updated_tenant:
        raise HTTPException(
            status_code=404,
            detail="Tenant not found"
        )

    return updated_tenant


# DELETE TENANT (Protected)
@router.delete("/{tenant_id}")
def remove_tenant(
    tenant_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):

    deleted_tenant = delete_tenant(
        db,
        tenant_id
    )

    if not deleted_tenant:
        raise HTTPException(
            status_code=404,
            detail="Tenant not found"
        )

    return {
        "message": "Tenant deleted successfully"
    }