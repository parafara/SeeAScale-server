import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_mail(To: str, Message: str):
    msg = EmailMessage()
    msg.set_content(Message)
    msg['To'] = To
    msg['From'] = "seeascale.auth@gmail.com"
    msg['Subject'] = "[See A Scale] 회원가입 이메일 인증"

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login("seeascale.auth@gmail.com", EMAIL_PASSWORD)
        server.send_message(msg)
