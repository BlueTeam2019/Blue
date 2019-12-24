from flask import Flask, request
import os, sys, smtplib
from email.mime.text import MIMEText as text

def send_report(exec_tests_pass,exec_tests_results, to):
    result = True
    gmail_user = 'ci.server.blue'
    gmail_password = 'ci.server.blue123'
    sent_from = gmail_user
    message = 'Build completed successfully'
    body = message
    if not exec_tests_pass:
        message = 'Build failed'
        body=  ", ".join(exec_tests_results)
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

