from flask import Flask, request
import os, sys, smtplib
from email.mime.text import MIMEText as text

def send_report(success,results, pusher_email, commit_hash, branch_name):
    result = True
    gmail_user = 'ci.server.blue@gmail.com'
    gmail_password = 'ci.server.blue123'
    sent_from = gmail_user
    to = [pusher_email,'lehacohen160@gmail.com']

    message = 'Build completed successfully'
    body = message
    if not success:
        message = 'Build failed'
        str = "Build faild. \ncommit hash: %s \nbranch name: %s \n" %(commit_hash, branch_name) 
        body = str + ", ".join(results)
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
