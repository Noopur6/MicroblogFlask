'''
Created on Apr 5, 2019

@author: nsno
'''
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User
from sqlalchemy import or_
from flask_babel import _, lazy_gettext as _l

class LoginForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))
    
class RegistrationForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_('Please use a different username.'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_('Please use a different email address.'))
        
class EditProfileForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    about_me = TextAreaField(_l('About Me'), validators=[Length(min=0, max=140)])
    submit = SubmitField(_l('submit'))
    
    def __init__(self, original_username, original_email, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username_email(self, username, email):
        if username != self.original_username or email!=self.original_email:
            user = User.query.filter(or_(username==self.username.data, email==self.email.data)).first()
            if user is not None:
                return False
                #raise ValidationError('Please use a different username.')
            
class PostForm(FlaskForm):
    post = TextAreaField(_l('Post something'), validators=[DataRequired(),Length(min=1, max=140)])
    submit = SubmitField(_l('submit'))
    
class PasswordResetRequestForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('submit'))
    
class ResetPasswordForm(FlaskForm):
    new_password = PasswordField(_l('New Password'), validators=[DataRequired()])
    confirm_new_password = PasswordField(_l('Confirm New Password'), validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField(_l('Request Password Reset'))