from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Property
from app.schemas import PropertyCreate
from app.auth.dependencies import get_current_user
from app.auth.rbac import admin_required

from app.crud.property_crud import (
    get_properties,
    update_property,
    delete_property
)

from app.crud.audit_crud import create_audit_log

router = APIRouter(
    prefix="/properties",
    tags=["Properties"]
)


# CREATE PROPERTY
@router.post("/")
def create_property(
    property: PropertyCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    new_property = Property(
        property_name=property.property_name,
        address=property.address,
        rent_amount=property.rent_amount
    )

    db.add(new_property)
    db.commit()
    db.refresh(new_property)

    # Audit log
    create_audit_log(
        db,
        current_user.email,
        f"Added Property ID: {new_property.id}"
    )

    return new_property


# GET ALL PROPERTIES
@router.get("/")
def view_properties(
    db: Session = Depends(get_db)
):

    return get_properties(db)


# UPDATE PROPERTY
@router.put("/{property_id}")
def edit_property(
    property_id: int,
    property_data: PropertyCreate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
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

    create_audit_log(
        db,
        current_user.email,
        f"Updated Property ID: {property_id}"
    )

    return updated_property


# DELETE PROPERTY
@router.delete("/{property_id}")
def remove_property(
    property_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
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


# TEST ADMIN ACCESS
@router.get("/test-admin")
def test_admin(
    current_user=Depends(admin_required)
):

    return {
        "message": "Admin Access Granted",
        "current_user": current_user
    }