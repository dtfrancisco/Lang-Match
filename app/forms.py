from flask_wtf import FlaskForm
from app.models import User
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired, Email, EqualTo, Length, ValidationError
import re


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(), Length(max=80, message='Email address cannot exceed 80 characters')])
    username = StringField('Username', validators=[InputRequired(), Length(max=40, message='Username cannot exceed 40 characters')])
    password = PasswordField('Password', validators=[InputRequired(), EqualTo('conf_password', message='Passwords must match'), Length(min=8, max=40, message='Password must be between 8 and 40 characters')])
    conf_password = PasswordField('Confirm Password', validators=[InputRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username has already been taken')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('An account with this email address already exists!')


class AnswerForm(FlaskForm):
    body = TextAreaField('', validators=[Length(min=0, max=500)])
    submit = SubmitField('Submit')


class SettingsForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(), Length(max=80, message='Email address cannot exceed 80 characters')])
    username = StringField('Username', validators=[InputRequired(), Length(max=40, message='Username cannot exceed 40 characters')])
    gender = SelectField('Gender', choices=[('m', 'Male'), ('f', 'Female'), ('o', 'Other')])
    birthday = DateField('Birthday', format='%Y-%m-%d')
    city = StringField('City', validators=[Length(max=50, message='City cannot exceed 50 characters')])
    state = StringField('State', validators=[Length(max=30, message='State cannot exceed 30 characters')])
    zip_code = StringField('Zip code')
    submit = SubmitField('Submit')

    def validate_zipcode(self, zip_code):
        if len(zip_code != 0 or zip_code != 5):
            raise ValidationError('Zip codes must be exactly 5 characters!')
        if len(zip_code == 5):
            if re.match('\d{5}', zip_code) is None:
                raise ValidationError('Zip codes may only contain digits!')
