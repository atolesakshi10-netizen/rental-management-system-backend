from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import Date
from sqlalchemy import Date
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

class AuditLog(Base):

    __tablename__ = "audit_logs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_email = Column(String)

    action = Column(String)

    timestamp = Column(
        DateTime,
        default=datetime.utcnow
    )
class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, unique=True)

    email = Column(String, unique=True)

    hashed_password = Column(String)

    role = Column(String, default="admin")
class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    property_name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    rent_amount = Column(Float, nullable=False)

class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    tenant_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=False)

class Agreement(Base):

    __tablename__ = "agreements"

    id = Column(Integer, primary_key=True, index=True)

    property_id = Column(Integer, nullable=False)
    tenant_id = Column(Integer, nullable=False)

    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    monthly_rent = Column(Float, nullable=False)

    blockchain_hash = Column(String)

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    agreement_id = Column(Integer, nullable=False)

    amount = Column(Float, nullable=False)

    payment_date = Column(Date, nullable=False)

    payment_status = Column(String, nullable=False)

    blockchain_hash = Column(String)