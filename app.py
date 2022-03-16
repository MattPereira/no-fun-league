
from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from forms import RegisterForm, LoginForm, EditUserForm
from sqlalchemy.exc import IntegrityError

from logic import get_roster
import requests
import os

app = Flask(__name__)


# The .replace fixes the error caused by heroku because heroku not up to date with latest sqlalchemy version

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    'DATABASE_URL', "postgres:///no_fun_league").replace("://", "ql://", 1)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = os.environ.get(
    'SECRET_KEY', 'miataisalwaystheanswer')
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)

toolbar = DebugToolbarExtension(app)


@app.route('/')
def home_page():
    """redirect to /register"""

    return render_template('index.html')


@app.route('/register', methods=["GET", "POST"])
def register_user():
    """show register form and handle user registration"""

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(
            username, password, email, first_name, last_name)
        db.session.add(new_user)

        try:
            db.session.commit()
        except IntegrityError:
            flash('Username is already taken', 'danger')
            return redirect('/register')

        session['username'] = new_user.username
        flash('Welcome! Successfully Created Your Account!', "success")
        return redirect(f'/users/{new_user.username}')

    return render_template('users/register.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login_user():
    """show login form and handle user login"""

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            flash(f"Welcome back, {user.username}!", "success")
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Invalid username/password']

    return render_template('users/login.html', form=form)


@app.route('/logout', methods=["POST"])
def logout_user():
    """Handle logout of user using session.pop('username')"""
    session.pop('username')
    flash("You have been logged out!", "info")
    return redirect('/')


@app.route('/users/<username>')
def show_user(username):
    """Show information about a user AND show all user submitted feedback"""

    if 'username' not in session or username != session['username']:
        return render_template('401.html')

    user = User.query.get_or_404(username)

    user_res = requests.get(f"https://api.sleeper.app/v1/user/{user.username}")
    user_data = user_res.json()

    user_id = user_data['user_id']

    league_res = requests.get(
        f"https://api.sleeper.app/v1/league/723677559673409536/rosters")

    league_data = league_res.json()

    # roster = get_roster(league_data, user_id)

    print('***************')
    print(league_data[6]['owner_id'])
    print(user_id)
    print(league_data[6]['owner_id'] == user_id)
    print('************')
    for owner in league_data:
        if owner['owner_id'] == user_id:
            roster = owner
        else:
            roster = 'wtf'

    return render_template('users/show.html', user=user, user_data=user_data, league_data=league_data, roster=roster)


@app.route('/users/<username>/update', methods=["GET", "POST"])
def edit_user(username):
    """Allow user to edit information about themself"""

    user = User.query.get_or_404(username)

    form = EditUserForm(obj=user)

    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data

        db.session.commit()
        session['username'] = user.username
        flash(
            f"Successfully updated {user.username}'s information!", "success")
        return redirect(f'/users/{user.username}')

    return render_template('users/edit.html', user=user, form=form)
