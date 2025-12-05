# src/utils/mailer.py
import os
import yagmail

def send_email(to, subject, body, attachment=None):
    EMAIL = os.getenv("EMAIL")
    APP_PASSWORD = os.getenv("APP_PASSWORD")
    yag = yagmail.SMTP(EMAIL, APP_PASSWORD)
    yag.send(to=to, subject=subject, contents=body, attachments=attachment)
