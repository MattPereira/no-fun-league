
from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Player
from forms import RegisterForm, LoginForm, EditUserForm


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

    if "user_id" in session:
        return redirect(f"/users/{session['user_id']}")

    form = RegisterForm()

    if form.validate_on_submit():
        user_id = form.user_id.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        password = form.password.data
        email = form.email.data

        new_user = User.register(
            user_id, first_name, last_name, password, email)
        db.session.add(new_user)

        db.session.commit()

        session['user_id'] = new_user.user_id
        flash('Welcome! Successfully Created Your Account!', "success")
        return redirect(f'/users/{new_user.user_id}')

    return render_template('users/register.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login_user():
    """show login form and handle user login"""

    if "user_id" in session:
        return redirect(f"/users/{session['user_id']}")

    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.authenticate(email, password)

        if user:
            flash(f"Welcome back!", "success")
            session['user_id'] = user.user_id
            return redirect(f'/users/{user.user_id}')
        else:
            form.email.errors = ['Invalid email/password']

    return render_template('users/login.html', form=form)


@app.route('/logout', methods=["POST"])
def logout_user():
    """Handle logout of user using session.pop('username')"""
    session.pop('user_id')
    flash("You have been logged out!", "info")
    return redirect('/')


@app.route('/users/<user_id>')
def show_user(user_id):
    """Show information about a user AND show all user submitted feedback"""

    user = User.query.get_or_404(user_id)

    user_res = requests.get(f"https://api.sleeper.app/v1/user/{user.user_id}")

    # figure out how to destructure this for just 'avatar' and 'username'
    user_data = user_res.json()

    league_res = requests.get(
        f"https://api.sleeper.app/v1/league/723677559673409536/rosters")

    league_data = league_res.json()

    roster = get_roster(league_data, user.user_id)

    return render_template('users/show.html', user=user, user_data=user_data, league_data=league_data, roster=roster)


@app.route('/users/<user_id>/update', methods=["GET", "POST"])
def edit_user(user_id):
    """Allow user to edit information about themself"""

    user = User.query.get_or_404(user_id)

    if 'user_id' not in session or user.user_id != session['user_id']:
        return render_template('401.html')

    form = EditUserForm(obj=user)

    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.email = form.email.data
        # come back to figure out how to allow password changing?

        db.session.commit()
        session['user_id'] = user.user_id
        flash(
            f"Successfully updated your information!", "success")
        return redirect(f'/users/{user.user_id}')

    return render_template('users/edit.html', user=user, form=form)


@app.route('/rosters', methods=['GET'])
def show_rosters():

    roster_res = requests.get(
        "https://api.sleeper.app/v1/league/723677559673409536/rosters")

    rosters = roster_res.json()

    users_res = requests.get(
        'https://api.sleeper.app/v1/league/723677559673409536/users')

    # users contains avatars but not all teams have one set properly
    # let users choose avatar url in form and store in database instead?
    users = users_res.json()

    return render_template('rosters.html', rosters=rosters, users=users)


@app.route('/draftboard', methods=["GET"])
def show_draftboard():

    res = requests.get(
        'https://api.sleeper.app/v1/draft/723677560327737344/picks')

    draft_res = res.json()

    return render_template('draftboard.html', draftboard=draft_res)


@app.route('/transactions', methods=['GET'])
def show_transactions():
    """Display league transactions, maybe with search by player or week functionality?"""

    # API call returns only 1 specific week at a time
    res = requests.get(
        "https://api.sleeper.app/v1/league/723677559673409536/transactions/1")

    transactions = res.json()

    return render_template('transactions.html', transactions=transactions)


@app.route('/blog', methods=['GET'])
def show_blog():

    return render_template('blog.html')


@app.route('/voting', methods=['GET'])
def show_voting():

    return render_template('voting.html')


@app.route('/fetch_players', methods=["GET"])
def fetch_players():

    res = requests.get("https://api.sleeper.app/v1/players/nfl")

    player_data = res.json()

    for player in player_data:
        p = Player(
            id=player['id'],
            first_name=player['first_name'],
            last_name=player['last_name'],
            position=player['position'],
            team=player['team'],
            age=player['age'],
            height=player['height']
        )

        db.session.add(p)
        db.session.commit()

    return redirect('/')
