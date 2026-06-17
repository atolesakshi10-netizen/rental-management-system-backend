from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.routes.auth_routes import router as auth_router
from app.routes import property_routes
from app.routes import tenant_routes
from app.routes import agreement_routes
from app.routes import payment_routes
from app.routes import dashboard_routes
from app.routes import audit_routes

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Rental Management System"
)

app.include_router(auth_router)

@app.get("/")
def home():
    return {"message": "Rental Management System API Running"}

app.include_router(
    property_routes.router
)

app.include_router(
    tenant_routes.router
)

app.include_router(
    agreement_routes.router
)

app.include_router(
    payment_routes.router
)

app.include_router(
    dashboard_routes.router
)

app.include_router(
    audit_routes.router
)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "service": "Rental Management System"
    }