from app.services.email_service import send_email

send_email(
    "your_own_email@gmail.com",
    "Test Mail",
    "Hello from FastAPI"
)