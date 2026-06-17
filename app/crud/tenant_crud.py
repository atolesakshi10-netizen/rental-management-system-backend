from sqlalchemy.orm import Session

from app.models import Tenant
from app.schemas import TenantCreate


def create_tenant(
    db: Session,
    tenant_data: TenantCreate
):

    new_tenant = Tenant(
        tenant_name=tenant_data.tenant_name,
        email=tenant_data.email,
        phone=tenant_data.phone
    )

    db.add(new_tenant)
    db.commit()
    db.refresh(new_tenant)

    return new_tenant


def get_tenants(db: Session):

    return db.query(Tenant).all()


def update_tenant(
    db: Session,
    tenant_id: int,
    tenant_data: TenantCreate
):

    tenant = db.query(Tenant).filter(
        Tenant.id == tenant_id
    ).first()

    if not tenant:
        return None

    tenant.tenant_name = tenant_data.tenant_name
    tenant.email = tenant_data.email
    tenant.phone = tenant_data.phone

    db.commit()
    db.refresh(tenant)

    return tenant


def delete_tenant(
    db: Session,
    tenant_id: int
):

    tenant = db.query(Tenant).filter(
        Tenant.id == tenant_id
    ).first()

    if not tenant:
        return None

    db.delete(tenant)
    db.commit()

    return tenant