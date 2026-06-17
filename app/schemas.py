from pydantic import BaseModel, EmailStr
from datetime import date
from datetime import date

class UserCreate(BaseModel):

    username: str

    email: str

    password: str

    role: str = "admin"

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True

class PropertyCreate(BaseModel):
    property_name: str
    address: str
    rent_amount: float


class PropertyResponse(PropertyCreate):
    id: int

    class Config:
        from_attributes = True       

class TenantCreate(BaseModel):
    tenant_name: str
    email: str
    phone: str


class TenantResponse(TenantCreate):
    id: int

    class Config:
        from_attributes = True

class AgreementCreate(BaseModel):
    property_id: int
    tenant_id: int
    start_date: date
    end_date: date
    monthly_rent: float


class AgreementResponse(AgreementCreate):
    id: int

    class Config:
        from_attributes = True

class PaymentCreate(BaseModel):
    agreement_id: int
    amount: float
    payment_date: date
    payment_status: str


class PaymentResponse(PaymentCreate):
    id: int

    class Config:
        from_attributes = True