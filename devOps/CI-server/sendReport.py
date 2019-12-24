from flask import Flask, request
import os, sys, smtplib
from email.mime.text import MIMEText as text

def send_report(success,file_fails, pusher_email):
    result = True
    gmail_user = 'ci.server.blue@gmail.com'
    gmail_password = 'ci.server.blue123'
    sent_from = gmail_user
    to = [pusher_email]

    message = 'Build completed successfully'
    body = message
    if not success:
        message = 'Build failed'
        with open (file_fails, "r") as file_fails:
            body = file_fails.read()
    subject = message
    msg = text(body)
    msg['Subject'] = subject
    msg['From'] = sent_from
    msg['To'] = ", ".join(to)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, msg.as_string())
        server.close()
    except Exception as err:
        print(err)
        print('Something went wrong...')
        result = False

    return result

