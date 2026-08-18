"""
Sends the emails built by email_content.py.

Deliverability notes (why emails land in spam, and what this addresses):

1. Multipart message (HTML + plain text) - a message with ONLY an HTML part
   looks more like a marketing blast to spam filters. We always attach both.
2. Real, matching From name/address - "From: Sky Briefing <you@yourdomain>",
   not a generic no-reply@ with a mismatched display name.
3. Personalized content - see email_content.py. Every recipient's message
   has different numbers and wording because it's built from their own
   city's weather, not one shared template blasted to everyone.
4. No spam-trigger language - avoid ALL CAPS subject lines, excessive
   exclamation marks, and words like "FREE"/"ACT NOW" in the subject/body.
5. Unsubscribe link present - required by law in many places (CAN-SPAM,
   GDPR) and its absence is itself a spam signal.
6. Authenticate properly - use a real SMTP account with an app password
   (not a hardcoded plaintext password in code), and ideally a domain with
   SPF/DKIM set up if you're sending at any volume. Gmail's own SMTP server
   already has good sender reputation, which helps for small/personal use.

None of this GUARANTEES inbox placement - reputation builds over time - but
it removes the obvious, avoidable red flags.
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
FROM_NAME = os.environ.get("FROM_NAME", "Sky Briefing")
FROM_EMAIL = os.environ.get("FROM_EMAIL", SMTP_USER)


def send_email(to_address, subject, html_body, plain_body):
    """
    Send one personalized email. Raises if SMTP credentials aren't set up,
    so failures are obvious instead of silently doing nothing.
    """
    if not SMTP_USER or not SMTP_PASSWORD:
        raise RuntimeError(
            "SMTP_USER / SMTP_PASSWORD not set. Copy .env.example to .env "
            "and fill in your email credentials (use an app password, not "
            "your real account password)."
        )

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = formataddr((FROM_NAME, FROM_EMAIL))
    msg["To"] = to_address

    # Attach plain text FIRST, then HTML - email clients use the last part
    # that they know how to render, so this order lets plain-text-only
    # clients fall back gracefully.
    msg.attach(MIMEText(plain_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(FROM_EMAIL, to_address, msg.as_string())
