import smtplib
from contextlib import contextmanager
from email.message import EmailMessage
from app.services.config import Config

config = Config()

@contextmanager
def get_smtp():
    """Provide an SMTP connection like a dependency generator."""
    timeout = 5
    if config.SMTP_SECURE:
        server = smtplib.SMTP_SSL(config.SMTP_HOST, config.SMTP_PORT, timeout=timeout)
    else:
        server = smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT, timeout=timeout)
        server.ehlo()
    try:
        if config.SMTP_USER and config.SMTP_PASSWORD:
            server.login(config.SMTP_USER, config.SMTP_PASSWORD)
        yield server
    finally:
        server.quit()

def send_mail(sender, recipient, subject, body_html=None, body_text=None):
    """
    Send an email that can include HTML and/or plain text.

    :param sender: sender email
    :param recipient: recipient email
    :param subject: email subject
    :param body_html: HTML content
    :param body_text: plain text content
    """
    msg = EmailMessage()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject

    if body_html and body_text:
        msg.set_content(body_text)
        msg.add_alternative(body_html, subtype='html')
    elif body_html:
        msg.set_content("This email contains HTML content. Please view in an HTML-compatible client.")
        msg.add_alternative(body_html, subtype='html')
    elif body_text:
        msg.set_content(body_text)
    else:
        raise ValueError("At least one of body_html or body_text must be provided")

    with get_smtp() as server:
        server.send_message(msg)
