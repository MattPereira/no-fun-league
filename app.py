
from flask import Flask, render_template, redirect, session, flash, jsonify, g
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Player, Roster, Manager, Pick, Post, Proposal, ProposalVotes
from forms import RegisterForm, LoginForm, EditUserForm, BlogForm

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


@app.before_request
def add_info_to_g():
    """Add managers, rosters, and user to Flask global"""

    # allows for dropdown links to display through base.html
    g.managers = Manager.query.all()
    g.rosters = Roster.query.all()

    # Add current user to 'g' if they are logged in
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])

    else:
        g.user = None


def do_login(user):
    """Log in a user"""

    session['user_id'] = user.id


def do_logout():
    """Logout a user."""

    if 'user_id' in session:
        del session['user_id']


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
    """Handle logout of user"""
    do_logout()
    flash("You have been logged out!", "info")
    return redirect('/')


@app.route('/')
def home_page():
    """redirect to /register"""

    return render_template('index.html')


@app.route('/users/<user_id>')
def show_user(user_id):
    """Show information about a user AND show all user submitted feedback"""

    user = User.query.get_or_404(user_id)

    return render_template('users/show.html', user=user)


@app.route('/users/<user_id>/update', methods=["GET", "POST"])
def edit_user(user_id):
    """Allow user to edit information about themself"""

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


@app.route('/managers/<int:user_id>')
def show_manager(user_id):
    """Show details about a manager"""

    user = User.query.get(user_id)
    manager = user.manager

    return render_template('league/manager.html', manager=manager)


@app.route('/rosters/<int:roster_id>')
def show_roster(roster_id):
    """Show details for a specific roster"""

    roster = Roster.query.get(roster_id)

    players = Player.query.filter(Player.id.in_(
        roster.player_ids)).order_by('position').all()

    return render_template('league/roster.html', roster=roster, players=players)


@app.route('/draftboard', methods=["GET", "POST"])
def show_draftboard():

    t1 = Pick.query.filter(Pick.roster_id == 1).order_by('id').all()
    t2 = Pick.query.filter(Pick.roster_id == 2).order_by('id').all()
    t3 = Pick.query.filter(Pick.roster_id == 3).order_by('id').all()
    t4 = Pick.query.filter(Pick.roster_id == 4).order_by('id').all()
    t5 = Pick.query.filter(Pick.roster_id == 5).order_by('id').all()
    t6 = Pick.query.filter(Pick.roster_id == 6).order_by('id').all()
    t7 = Pick.query.filter(Pick.roster_id == 7).order_by('id').all()
    t8 = Pick.query.filter(Pick.roster_id == 8).order_by('id').all()
    t9 = Pick.query.filter(Pick.roster_id == 9).order_by('id').all()
    t10 = Pick.query.filter(Pick.roster_id == 10).order_by('id').all()

    draft_picks = [t1, t2, t3, t4, t5, t6, t7, t8, t9, t10]

    return render_template('league/draftboard.html', t1=t1, t2=t2, t3=t3, t4=t4, t5=t5, draft=draft_picks)


@app.route('/blog', methods=['GET'])
def show_blog():
    """Show all blog posts by order of most recent"""
    posts = Post.query.order_by(Post.created_at.desc()).all()

    return render_template('league/blog/blog.html', posts=posts)


@app.route('/blog/new', methods=["GET", "POST"])
def add_post():
    """Show form if GET, handle creating new blog post if POST"""

    if not g.user:
        flash("Sorry, you must be logged in to create a blog post!", "danger")
        return redirect('/blog')

    form = BlogForm()

    if form.validate_on_submit():
        post = Post(user_id=g.user.id, title=form.title.data,
                    content=form.content.data)
        db.session.add(post)
        db.session.commit()

        flash(f"{g.user.first_name} has successfully create a blog post!", "success")
        return redirect('/blog')

    return render_template('league/blog/new.html', form=form)


@app.route('/blog/<int:post_id>/edit', methods=["GET", "POST"])
def edit_post(post_id):
    """Handle display of edit form and editing a blog post"""

    if not g.user:
        flash("Sorry, you must be logged in to edit your blog post!", "danger")
        return redirect('/blog')

    post = Post.query.get(post_id)

    if post.user_id != g.user.id:
        flash("You may only edit your own posts!", "danger")
        return redirect('/blog')

    form = BlogForm(obj=post)

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()

        flash("You have successfully edited your post!", "success")
        return redirect('/blog')

    return render_template('league/blog/edit.html', form=form, post=post)


@app.route('/blog/<int:post_id>/delete', methods=["POST"])
def destroy_post(post_id):
    """Handle deletion of a blog post"""

    if not g.user:
        flash("Sorry, you must be logged in to delete your blog post!", "danger")
        return redirect('/blog')

    post = Post.query.get(post_id)

    if post.user_id != g.user.id:
        flash("You may only delete your own posts!", "danger")
        return redirect('/blog')

    db.session.delete(post)
    db.session.commit()
    flash("You have successfully deleted your post!", "success")

    return redirect('/blog')


@app.route('/polls', methods=['GET'])
def show_polls():
    """Show all rule proposals and user submitted votes"""
    proposals = Proposal.query.all()

    return render_template('league/polls.html', proposals=proposals)
