import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import bleach


class Email:
    def __init__(
        self,
        droid,
        smtp_host,
        smtp_port,
        smtp_username,
        smtp_password,
        default_from_email="",
    ):
        self.droid = droid
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
        self.default_from_email = default_from_email

    def send(self, subject, to_email, from_email="", body_text="", body_html=""):
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = from_email or self.default_from_email
        message["To"] = to_email

        if body_text:
            message.attach(MIMEText(body_text, "plain"))

        if body_html:
            message.attach(MIMEText(body_html, "html"))

        if body_html and not body_text:
            plain = bleach.clean(body_html)
            message.attach(MIMEText(plain, "plain"))

        with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
            server.login(self.smtp_username, self.smtp_password)
            server.sendmail(message["From"], to_email, message.as_string())
