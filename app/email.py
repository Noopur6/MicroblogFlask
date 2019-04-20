'''
Created on Apr 18, 2019

@author: nsno
'''
from flask_mail import Message
from app import mail, microblogapp
from flask.templating import render_template

def send_mail(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)
    
def send_password_reset_mail(user):
    token = user.get_reset_password_token()
    print("token generated:"+token)
    send_mail('Microblog: Reset your password', sender=microblogapp.config['ADMINS'][0], recipients=[user.email], 
              text_body= render_template('email/reset_password.txt', user=user, token=token), 
              html_body=render_template('email/reset_password.html', user=user, token=token))