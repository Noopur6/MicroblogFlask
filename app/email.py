'''
Created on Apr 18, 2019

@author: nsno
'''
from flask_mail import Message
from app import mail

def send_mail(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)
    
def send_password_reset_mail(user):
    return 