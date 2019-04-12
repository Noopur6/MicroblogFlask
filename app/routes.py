'''
Created on Apr 1, 2019

@author: NSNO
'''
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user,logout_user
from app import microblogapp
from app.models import User
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from flask_login import login_required
from werkzeug.urls import url_parse
from app import db
from datetime import datetime

@microblogapp.route('/index')
@login_required #makes the url protected, makes login necessary
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
    #return render_template('index.html', title='Home', user=user, posts=posts)
    return render_template('index.html', title='Home', posts=posts)

#This method renders login page on login GET request
# and submits the user login data on POST login request
@microblogapp.route('/login', methods=['GET','POST'])
def login():
    #a user that is logged in, and the user navigates to the /login URL of your application, restricted
    if current_user.is_authenticated:#current_user to obtain the user object that represents the client of the request
        return redirect(url_for('index'))
    form = LoginForm()
    #In the GET request, no form, return False
    #in the POST request, gather data, run form validators and return True/False
    if form.validate_on_submit():
        #query the database for matching username, and return the first object as there will b only 1 user by that username
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.verify_password(form.password.data):
            ## just flashing message
            flash('Invalid username or password')
            return redirect(url_for('login'))##the parameter is the method name not the url
        #this method registers a user as logged on by setting the value of current_user in the session
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@microblogapp.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('/index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congrats! you have been successfully registered!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
    
@microblogapp.route('/user/<username>') #path variable
@login_required
def user(username):#value of the path variable is stored in this parameter
    user = User.query.filter_by(username= username).first_or_404()
    posts = [{'author':user, 'body':'Test post 1'}, {'author':user, 'body':'Test post 2'}]
    return render_template('user.html', user=user, posts=posts)

@microblogapp.route('/edit_profile', methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():#if true, then save the entered data to db
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('your changes have been saved')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':#if it is a get request, pre-populate the fields with already saved data
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        return render_template('edit_profile.html', title='Edit Profile', form=form)

@microblogapp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    
@microblogapp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))