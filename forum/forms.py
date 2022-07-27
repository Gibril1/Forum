from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, ValidationError
from wtforms.validators import DataRequired, Length, EqualTo, Email
# from email_validator import validate_email

from forum.models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=
    [DataRequired(), Length(min=5,max=10)])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=
    [DataRequired(), Length(min=5,max=10)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password')
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username has been taken already')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email has been taken already')