from tokenize import String
from typing import Text
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, TextAreaField, BooleanField
from wtforms.validators import InputRequired, Email, Length, NumberRange
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
    location = StringField("Location", validators=[
        InputRequired(), Length(max=25)])
    ff_since = IntegerField("Playing Fantasy Football Since", validators=[
                            NumberRange(min=1900, max=2100)])
    fav_team = StringField("Favorite Team", validators=[
                           InputRequired(), Length(min=3, max=3)])
    bio = TextAreaField("About Me")
    philosophy = TextAreaField("Team Philosophy")


class FetchDraftForm(FlaskForm):
    """leave this blank"""
