from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.audit_crud import create_audit_log
from app.database import get_db
from app.schemas import PropertyCreate
from app.auth.dependencies import get_current_user
from app.auth.rbac import admin_required

from app.crud.property_crud import (
    create_property,
    get_properties,
    update_property,
    delete_property
)

router = APIRouter(
    prefix="/properties",
    tags=["Properties"]
)


# CREATE PROPERTY (Protected)
@router.post("/")
def add_property(
    property_data: PropertyCreate,
    db: Session = Depends(get_db),
    current_user = Depends(admin_required)
):

    new_property = create_property(
        db,
        property_data
    )

    create_audit_log(
        db,
        current_user.email,
        f"Created Property: {new_property.property_name}"
    )

    return new_property
# GET ALL PROPERTIES (Public)
@router.get("/")
def view_properties(
    db: Session = Depends(get_db)
):
    return get_properties(db)


# UPDATE PROPERTY (Protected)
@router.put("/{property_id}")
def edit_property(
    property_id: int,
    property_data: PropertyCreate,
    db: Session = Depends(get_db),
    current_user = Depends(admin_required)
):

    updated_property = update_property(
        db,
        property_id,
        property_data
    )

    if not updated_property:
        raise HTTPException(
            status_code=404,
            detail="Property not found"
        )

    return updated_property


# DELETE PROPERTY (Protected)
@router.delete("/{property_id}")
def remove_property(
    property_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(admin_required)
):

    deleted_property = delete_property(
        db,
        property_id
    )

    if not deleted_property:
        raise HTTPException(
            status_code=404,
            detail="Property not found"
        )

    create_audit_log(
        db,
        current_user.email,
        f"Deleted Property ID: {property_id}"
    )

    return {
        "message": "Property deleted successfully"
    }

@router.get("/test-admin")
def test_admin(
    current_user = Depends(admin_required)
):
    return {
        "message": "Admin Access Granted"
    }