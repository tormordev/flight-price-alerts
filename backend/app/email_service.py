import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
import os
from sendgrid import SendGridAPIClient

SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
HOST_MAIL = os.getenv('HOST_MAIL')


def send_email(to_email, subject, content):
    message = Mail(
        from_email=os.getenv("HOST_MAIL"),
        to_emails=to_email,
        subject=subject,
        html_content=content,
    )
    try:
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        response = sg.send(message)
        if response.status_code == 202:
            return {"status_code": response.status_code, "message": "Email sent successfully"}
        else:
            return {"status_code": response.status_code, "error": response.body.decode("utf-8")}
    except Exception as e:
        return {"error": str(e)}