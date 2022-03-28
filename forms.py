from tokenize import String
from typing import Text
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, TextAreaField, BooleanField, SelectField
from wtforms.validators import InputRequired, Email, Length, NumberRange
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


nfl_teams = [('sf', '49ers'), ('lar', 'Rams'),
             ('was', 'Commanders'), ('sea', 'Seahawks'), ('lv', 'Raiders'), ('cin', 'Bengals'), ('phi', 'Eagles'), ('chi', 'Bears'), ('dal', 'Cowboys'), ('tb', 'Buccaneers')]


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
    fav_team = SelectField("Favorite Team", choices=nfl_teams, validators=[
                           InputRequired()])
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
