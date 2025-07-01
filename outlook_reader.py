import os
import imaplib
import email
from email.header import decode_header
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

def get_unread_emails():
    imap = imaplib.IMAP4_SSL("mail.adm.tools")
    imap.login(EMAIL, PASSWORD)
    imap.select("inbox")

    status, messages = imap.search(None, 'UNSEEN')
    mail_ids = messages[0].split()
    emails_data = []

    for num in mail_ids:
        status, msg_data = imap.fetch(num, "(RFC822)")
        for part in msg_data:
            if isinstance(part, tuple):
                msg = email.message_from_bytes(part[1])

                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding or "utf-8", errors="ignore")

                from_ = msg.get("From")

                body = ""
                if msg.is_multipart():
                    for p in msg.walk():
                        if p.get_content_type() == "text/plain":
                            body = p.get_payload(decode=True).decode(errors="ignore")
                            break
                else:
                    if msg.get_content_type() == "text/plain":
                        body = msg.get_payload(decode=True).decode(errors="ignore")

                emails_data.append({
                    "from": from_,
                    "subject": subject,
                    "body": body.strip()
                })

    imap.logout()
    return emails_data
