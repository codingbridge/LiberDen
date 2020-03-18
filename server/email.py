# pylint: disable=missing-docstring
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.header import Header
from email.utils import parseaddr

def send_email(client, msg):
    client.send_message(msg)


def get_email_client(host, port, username, password):
    if port:
        client = smtplib.SMTP(host, port)
    else:
        client = smtplib.SMTP(host)

    client.login(username, password)
    return client

def get_email_message(sender, recipient, carbon_copy, blind_carbon_copy, subject, body):
    if not ('@' in parseaddr(sender)[1] and '@' in parseaddr(recipient)[1]):
        return None

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Cc'] = carbon_copy
    msg['Bcc'] = blind_carbon_copy
    msg['Subject'] = Header(subject, 'utf-8').encode()
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    return msg

def add_attachment(msg, attachment):
    with open(attachment, 'rb') as fp:
        if attachment.endswith(".pdf"):
            att = MIMEApplication(fp.read(), _subtype="pdf")
        else:
            att = MIMEImage(fp.read())
        att.add_header('Content-Disposition', 'attachment', filename=attachment)
        msg.attach(att)
    return msg
