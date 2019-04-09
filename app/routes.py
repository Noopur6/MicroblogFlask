'''
Created on Apr 1, 2019

@author: NSNO
'''
from flask import render_template, flash, redirect, url_for
from app import microblogapp
from app.forms import LoginForm

@microblogapp.route('/hello')
def hello():
    return "hello"

@microblogapp.route('/index')
def index():
    user = {"name":"noopur","age":23}
    posts = [
        {
            'author': {'username': 'Susan'},
            'body': 'How ya doin?'
        },
        {
            'author': {'username': 'Will'},
            'body': 'I think I will watch avengers..:)'    
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@microblogapp.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        ## just flashing message
        flash('Login requested for user {}, remember_me={}'.format(form.username.data,form.remember_me.data))
        return redirect(url_for('index'))##the parameter is the method name not the url
    return render_template('login.html', title='Sign In', form=form)