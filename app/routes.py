'''
Created on Apr 1, 2019

@author: NSNO
'''
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user,logout_user
from app import microblogapp
from app.models import User, Post
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm, PasswordResetRequestForm, ResetPasswordForm
from flask_login import login_required
from werkzeug.urls import url_parse
from app import db
from datetime import datetime
from app.email import send_password_reset_mail

@microblogapp.route('/', methods=['GET','POST'])
@microblogapp.route('/index', methods=['GET','POST'])
@login_required #makes the url protected, makes login necessary
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is live now!')
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(page, microblogapp.config['POSTS_PER_PAGE'], False)
    next_url = url_for('index',page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None
    #posts = current_user.followed_posts().all() #Calling all() on the query triggers its execution, 
    #with the return value being a list with all the results 
    return render_template('index.html', title='Home', posts=posts.items, form=form, prev_url=prev_url, next_url=next_url)

@microblogapp.route('/explore')
@login_required
def explore(): #request.args.get(key, default=None, type=None)
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, microblogapp.config['POSTS_PER_PAGE'], False)
    #posts = Post.query.order_by(Post.timestamp).all()
    next_url = url_for('explore', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html', title='Explore', posts=posts.items, next_url=next_url, prev_url=prev_url)

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
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(page, microblogapp.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user',username=username, page=posts.next_num) if posts.has_next else None
    prev_url = url_for('user', username=username, page=posts.prev_num) if posts.has_prev else None
    return render_template('user.html', user=user, posts=posts.items, next_url=next_url, prev_url=prev_url)

@microblogapp.route('/edit_profile', methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username, current_user.email) 
    if form.validate_on_submit() or form.validate_username_email(form.username.data, form.email.data):#if true, then save the entered data to db
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('your changes have been saved')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':#if it is a get request, pre-populate the fields with already saved data
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',form=form)

@microblogapp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User not found')
        return redirect(url_for('index'))
    elif user == current_user:
        flash('You cannot follow yourself')
        return redirect(url_for('index'))
    current_user.follow(user)
    db.session.commit()
    flash('You have successfully followed {}'.format(username))
    return redirect(url_for('user',username=username))

@microblogapp.route('/unfollow/<username>')
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User not found')
        return redirect(url_for('index'))
    elif user == current_user:
        flash('You cannot unfollow yourself')
        return redirect(url_for('index'))
    current_user.unfollow(user)
    db.session.commit()
    flash('You have successfully unfollowed {}'.format(username))
    return redirect(url_for('user',username=username))

@microblogapp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_mail(user)
            flash('Check your email for instructions to reset your password')
            return redirect(url_for('login'))
        else:
            flash('Enter email you used to sign up')
    return render_template('reset_password_request.html', title='Reset password', form=form)

@microblogapp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.new_password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)
        
@microblogapp.before_request
def before_request():  #this is called before every view function
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()#updating last seen value at every request
        db.session.commit()
    
@microblogapp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))