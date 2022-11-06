import os
import ssl
import jinja2
import smtplib
from datetime import datetime, timedelta
from typing import List, Union
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()
EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
MAIL_SERVER = os.environ.get("MAIL_SERVER")
MAIL_SERVER_ADDR = MAIL_SERVER.split(':')[0]
MAIL_SERVER_PORT = int(MAIL_SERVER.split(':')[1])


context = ssl.create_default_context()

templateLoader = jinja2.FileSystemLoader(searchpath="./src/templates")
templateEnv = jinja2.Environment(loader=templateLoader)


def send_email(msg: str, to_email: Union[str, List] = EMAIL_ADDRESS):
    try:
        with smtplib.SMTP(MAIL_SERVER_ADDR, MAIL_SERVER_PORT) as server:
            server.starttls(context=context)
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, to_email, msg)
            server.quit()
            print("Success: Email sent!")
            return True
    except Exception as e:
        print(e)
        print("Email failed to send.")
        return False


def send_signup_verification_email(subject: str, code: str, to_email: Union[str, List]):
    MESSAGE = MIMEMultipart('alternative')
    MESSAGE['subject'] = f"({code}) {subject}"
    MESSAGE['To'] = to_email
    MESSAGE['From'] = EMAIL_ADDRESS
    MESSAGE.preamble = """
    Your mail reader does not support the report format.
    Please visit us online!"""
    TEMPLATE_FILE = "general-verification-code.html"
    template = templateEnv.get_template(TEMPLATE_FILE)
    utcnow = datetime.utcnow()
    expireTime = timedelta(minutes=10) + utcnow
    body = template.render(event="Sign Up Email Verification", code=code,
                           expTimeIso=expireTime.isoformat() + 'Z', expireDuration=10)
    HTML_BODY = MIMEText(body, 'html')
    MESSAGE.attach(HTML_BODY)
    send_email(MESSAGE.as_string(), to_email)
