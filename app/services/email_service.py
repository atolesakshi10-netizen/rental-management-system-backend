import smtplib
from email.message import EmailMessage

SENDER_EMAIL = "atolesakshi38@gmail.com"
APP_PASSWORD = "yguglgvanbcvdimi"


def send_email(receiver_email: str, subject: str, body: str):

    if not receiver_email:
        raise Exception("Receiver email is empty")

    msg = EmailMessage()

    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email

    msg.set_content(body)

    try:

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:

            server.login(
                SENDER_EMAIL,
                APP_PASSWORD
            )

            server.send_message(msg)

        print(f"Email sent successfully to: {receiver_email}")

    except Exception as e:

        print("EMAIL ERROR:", e)
        raise e