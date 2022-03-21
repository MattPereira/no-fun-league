from tokenize import String
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField
from wtforms.validators import InputRequired, Email, Length
import email_validator


class RegisterForm(FlaskForm):
    user_id = StringField("Sleeper User_ID", validators=[
        InputRequired(), Length(max=50)])
    first_name = StringField("First Name", validators=[
                             InputRequired(), Length(max=30)])
    last_name = StringField("Last Name", validators=[
                            InputRequired(), Length(max=30)])
    email = StringField("Email", validators=[
                        InputRequired(), Email(), Length(min=5, max=50)])
    password = PasswordField("Password", validators=[InputRequired()])


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[
                        InputRequired(), Email(), Length(min=5, max=50)])
    password = PasswordField("Password", validators=[
                             InputRequired(), Length(min=7, max=30)])


class EditUserForm(FlaskForm):
    first_name = StringField("First Name", validators=[
                             InputRequired(), Length(max=30)])
    last_name = StringField("Last Name", validators=[
                            InputRequired(), Length(max=30)])
    email = StringField("Email", validators=[
                        InputRequired(), Email(), Length(min=5, max=50)])
