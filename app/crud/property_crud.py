from sqlalchemy.orm import Session

from app.models import Property
from app.schemas import PropertyCreate


# CREATE PROPERTY
def create_property(
    db: Session,
    property_data: PropertyCreate
):

    new_property = Property(
        property_name=property_data.property_name,
        address=property_data.address,
        rent_amount=property_data.rent_amount
    )

    db.add(new_property)
    db.commit()
    db.refresh(new_property)

    return new_property


# READ ALL PROPERTIES
def get_properties(db: Session):

    return db.query(Property).all()


# READ SINGLE PROPERTY
def get_property_by_id(
    db: Session,
    property_id: int
):

    return db.query(Property).filter(
        Property.id == property_id
    ).first()


# UPDATE PROPERTY
def update_property(
    db: Session,
    property_id: int,
    property_data: PropertyCreate
):

    property_obj = db.query(Property).filter(
        Property.id == property_id
    ).first()

    if not property_obj:
        return None

    property_obj.property_name = property_data.property_name
    property_obj.address = property_data.address
    property_obj.rent_amount = property_data.rent_amount

    db.commit()
    db.refresh(property_obj)

    return property_obj


# DELETE PROPERTY
def delete_property(
    db: Session,
    property_id: int
):

    property_obj = db.query(Property).filter(
        Property.id == property_id
    ).first()

    if not property_obj:
        return None

    db.delete(property_obj)
    db.commit()

    return property_obj