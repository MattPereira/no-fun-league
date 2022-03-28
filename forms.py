from ast import Pass
from tokenize import String
from typing import Text
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, TextAreaField, BooleanField, SelectField, SubmitField
from wtforms.validators import InputRequired, Email, Length, NumberRange, DataRequired, EqualTo, Optional
from choices import nfl_teams, positions, players, trades
import email_validator


class RegisterForm(FlaskForm):
    sleeper_id = SelectField("Sleeper Account", validators=[
        InputRequired()])
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
    location = StringField("Location", validators=[Optional()])
    fav_team = SelectField("Favorite Team", choices=nfl_teams, validators=[
                           InputRequired()])
    fav_position = SelectField(
        "Favorite Position", choices=positions, validators=[InputRequired()])
    fav_player = SelectField(
        "Favorite Player", choices=players, validators=[InputRequired()])
    trade_desire = SelectField('Desire to Trade', choices=trades)
    bio = TextAreaField("About Me")
    philosophy = TextAreaField("Team Philosophy")


class BlogPostForm(FlaskForm):
    title = StringField("Title", validators=[
                        InputRequired(), Length(max=100)])
    para_1 = TextAreaField("Paragraph One (Required)", validators=[
        InputRequired(), Length(max=750)])
    para_2 = TextAreaField("Paragraph Two (Optional)",
                           validators=[Length(max=750)])
    para_3 = TextAreaField("Paragraph Three (Optional)",
                           validators=[Length(max=750)])


class ProposalForm(FlaskForm):
    ammendment = StringField("Ammendment", validators=[
                             InputRequired(), Length(max=100)])
    argument = TextAreaField("Argument", validators=[Length(max=1000)])


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[
                             InputRequired(), Length(min=7, max=30)])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
