# Form classes for the application
# The WTForms classes will handle form validation and processing

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User

class LoginForm(FlaskForm):
# Form for user login

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
# Form for new user registratoin
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20, message='Your username must be between 2 and 20 characters')])
    email = StringField('Email', validators=[DataRequired(), Email(message='Please enter a valid email address')])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, message='Password must be at least 6 characters')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register')

    # Adding extra validation
    def validate_username(self, username):
        # Check if the username is already taken
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose another one.')
    def validate_email(self, email):
        # Check if email is already registered
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please choose another email')
        
class TicketCreateForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    priority = SelectField('Priority', choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], validators=[DataRequired()])
    submit = SubmitField('Create Ticket')


class TicketUpdateForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    priority = SelectField('Priority', choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], validators=[DataRequired()])
    status = SelectField('Status', choices=[('open', 'Open'), ('in_progress', 'In Progress'), ('closed', 'Closed')], validators=[DataRequired()])
    submit = SubmitField('Update Ticket')

class CommentForm(FlaskForm):
    # Form for adding comments to tickets

    content = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Add Comment')