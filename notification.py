import json
import smtplib
from email.mime import multipart

with open("config.json") as config:
    _CONFIG = json.load(config)


@staticmethod
def send_notification(message: str):
    server = smtplib.SMTP(_CONFIG['email']['server'], _CONFIG['email']['port'])
    server.starttls()
    server.login(_CONFIG['email']['username'], _CONFIG['email']['password'])

    msg = multipart.MIMEMultipart()
    msg['From'] = _CONFIG['email']['username']
    msg['To'] = _CONFIG['email']['username']
    msg['Subject'] = "Alert: {}".format(message)
    server.sendmail(_CONFIG['email']['username'], _CONFIG['email']['username'], msg.as_string())
