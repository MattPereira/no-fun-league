
from flask import Flask, render_template, redirect, session, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Player, Roster, Manager, Pick, Post
from forms import RegisterForm, LoginForm, EditUserForm


from logic import get_roster
import requests
import os
import json

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
        return redirect(f"/mangers/{session['user_id']}")

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

        session['user_id'] = new_user.id
        flash('Welcome to the No Fun League! Please edit your profile!', "success")
        return redirect(f'/managers/{new_user.manager.id}')

    return render_template('users/register.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login_user():
    """show login form and handle user login"""

    if "user_id" in session:
        return redirect(f"/")

    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.authenticate(email, password)

        if user:
            flash(f"Welcome back {user.first_name}!", "success")
            session['user_id'] = user.id
            return redirect(f'/managers/{user.id}')
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
    #### COME BACK TO FIGURE OUT PASSWORD CHANGING ####

    user = User.query.get_or_404(user_id)

    if 'user_id' not in session or user.id != session['user_id']:
        return render_template('401.html')

    form = EditUserForm(obj=user)

    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.email = form.email.data
        user.location = form.location.data
        user.ff_since = form.ff_since.data
        user.fav_team = form.fav_team.data
        user.bio = form.bio.data
        user.philosophy = form.philosophy.data

        db.session.commit()
        flash(
            f"Successfully updated {user.first_name}'s profile!", "success")
        return redirect(f'/managers/{user.id}')

    return render_template('users/edit.html', user=user, form=form)


@app.route('/managers')
def show_managers():
    """Show list of all managers with link to individual pages"""

    managers = Manager.query.all()

    return render_template('league/managers.html', managers=managers)


@app.route('/managers/<int:user_id>')
def show_manager(user_id):
    """Show details about a manager"""

    user = User.query.get(user_id)
    manager = user.manages[0]

    return render_template('league/manager.html', manager=manager)


@app.route('/rosters', methods=['GET'])
def show_rosters():

    rosters = Roster.query.all()

    return render_template('league/rosters.html', rosters=rosters)


@app.route('/rosters/<int:roster_id>')
def show_roster(roster_id):
    """Show details for a specific roster"""

    roster = Roster.query.get(roster_id)

    players = Player.query.filter(Player.id.in_(
        roster.players)).order_by('position').all()

    return render_template('league/roster.html', roster=roster, players=players)


@app.route('/draftboard', methods=["GET", "POST"])
def show_draftboard():

    r1 = Pick.query.filter(Pick.roster_id == 1).order_by('id').all()
    r2 = Pick.query.filter(Pick.roster_id == 2).order_by('id').all()
    r3 = Pick.query.filter(Pick.roster_id == 3).order_by('id').all()
    r4 = Pick.query.filter(Pick.roster_id == 4).order_by('id').all()
    r5 = Pick.query.filter(Pick.roster_id == 5).order_by('id').all()

    return render_template('league/draftboard.html', r1=r1, r2=r2, r3=r3, r4=r4, r5=r5)


@app.route('/blog', methods=['GET'])
def show_blog():
    """Show all blog posts by order of most recent"""
    posts = Post.query.order_by(Post.created_at.desc()).all()

    return render_template('league/blog.html', posts=posts)


@app.route('/polls', methods=['GET'])
def show_polls():

    return render_template('league/polls.html')


@app.route('/update_players', methods=["GET"])
def fetch_players():
    """Temporary route to fetch player info. can it be a get if it posts/patches data to local db?"""
    # players = requests.get("https://api.sleeper.app/v1/players/nfl")

    f = open('players.json', 'r')

    players = json.loads(f.read())

    for player in players.values():
        p = Player(id=player.get('player_id'), last_name=player.get('last_name'), full_name=player.get('full_name'),
                   position=player.get('position'), team=player.get('team'), age=player.get('age'), height=player.get('height'))

        db.session.add(p)
        db.session.commit()

    return players
