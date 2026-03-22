from contextlib import asynccontextmanager
from email.message import EmailMessage

import aiosmtplib

from app.services.config import Config

config = Config()

@asynccontextmanager
async def get_smtp_async():
    """Provide an async SMTP connection like a dependency generator."""
    if config.SMTP_SECURE:
        server = aiosmtplib.SMTP(
            hostname=config.SMTP_HOST,
            port=config.SMTP_PORT,
            use_tls=True,
            timeout=5
        )
    else:
        server = aiosmtplib.SMTP(
            hostname=config.SMTP_HOST,
            port=config.SMTP_PORT,
            use_tls=False,
            timeout=5
        )
    await server.connect()
    try:
        if config.SMTP_USER and config.SMTP_PASSWORD:
            await server.login(config.SMTP_USER, config.SMTP_PASSWORD)
        yield server
    finally:
        await server.quit()

async def send_mail_async(sender, recipient, subject, body_html=None, body_text=None):
    """
    Send an email asynchronously that can include HTML and/or plain text.
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

    async with get_smtp_async() as server:
        await server.send_message(msg)
