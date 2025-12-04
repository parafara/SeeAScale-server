import smtplib
from email.message import EmailMessage
from utils.constant import SMTP_SERVER_ADDRESS, SMTP_PORT, SMTP_MAIL_ADDRESS, SMTP_PASSWORD

def send_preregister_mail(To: str, Message: str):
    msg = EmailMessage()
    msg.set_content(Message)
    msg['To'] = To
    msg['From'] = SMTP_MAIL_ADDRESS
    msg['Subject'] = "[See A Scale] 회원가입 이메일 인증"

    with smtplib.SMTP_SSL(SMTP_SERVER_ADDRESS, SMTP_PORT) as server:
        server.login(SMTP_MAIL_ADDRESS, SMTP_PASSWORD)
        server.send_message(msg)
