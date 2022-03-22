
from flask import Flask, render_template, redirect, session, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Player, Roster, Member, Pick
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

    return render_template('users/show.html', user=user)


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

    rosters = Roster.query.all()

    return render_template('league/rosters.html', rosters=rosters)


@app.route('/draftboard', methods=["GET", "POST"])
def show_draftboard():

    r1 = Pick.query.filter(Pick.roster_id == 1).order_by('id').all()
    r2 = Pick.query.filter(Pick.roster_id == 2).order_by('id').all()
    r3 = Pick.query.filter(Pick.roster_id == 3).order_by('id').all()
    r4 = Pick.query.filter(Pick.roster_id == 4).order_by('id').all()
    r5 = Pick.query.filter(Pick.roster_id == 5).order_by('id').all()

    return render_template('league/draftboard.html', r1=r1, r2=r2, r3=r3, r4=r4, r5=r5)


@app.route('/transactions', methods=['GET'])
def show_transactions():
    """Display league transactions, maybe with search by player or week functionality?"""

    # API call returns only 1 specific week at a time
    res = requests.get(
        "https://api.sleeper.app/v1/league/723677559673409536/transactions/1")

    transactions = res.json()

    return render_template('league/transactions.html', transactions=transactions)


@app.route('/blog', methods=['GET'])
def show_blog():

    return render_template('league/blog.html')


@app.route('/voting', methods=['GET'])
def show_voting():

    return render_template('league/voting.html')


@app.route('/update_players', methods=["GET"])
def fetch_players():
    """NEEDS TONS OF WORK"""
    # res = requests.get("https://api.sleeper.app/v1/players/nfl")

    f = open('tiny_players.json', 'r')

    players = f.read()

    print('********************')
    print(players)
    print('********************')

    # for player in player_data:
    #     p = Player(
    #         id=player['id'],
    #         first_name=player['first_name'],
    #         last_name=player['last_name'],
    #         position=player['position'],
    #         team=player['team'],
    #         age=player['age'],
    #         height=player['height']
    #     )

    #     db.session.add(p)
    #     db.session.commit()

    return players
