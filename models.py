from email.policy import default
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

import datetime


db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = 'users'

    # user.id must be set to the unique sleeper ID
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    sleeper_id = db.Column(db.Text, unique=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    location = db.Column(db.String(25), default="mom's basement")
    ff_since = db.Column(db.Integer, default=2020)
    fav_team = db.Column(db.String, default='lar')
    bio = db.Column(db.String(500), default='i am to lazy to edit my bio')
    philosophy = db.Column(
        db.String(250), default='A procrastinator’s work is never done.')
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)

    def __repr__(self):
        u = self
        return f"<User id={u.id} first_name={u.first_name} last_name={u.last_name}>"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @classmethod
    def register(cls, sleeper_id, first_name, last_name, email, password):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(password)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        user = cls(
            sleeper_id=sleeper_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_utf8
        )
        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, email, password):
        """Validate that user exists & password is correct. Return user if valid; else return False."""

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            # return user instance
            return user
        else:
            return False


class Manager(db.Model):
    __tablename__ = 'managers'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Text, db.ForeignKey(
        'users.sleeper_id'), unique=True, nullable=False)
    display_name = db.Column(db.Text)
    avatar_id = db.Column(db.Text, default='15d7cf259bc30eab8f6120f45f652fb6')
    team_name = db.Column(db.Text)

    user = db.relationship('User', backref="manages")


class Pick(db.Model):
    __tablename__ = "picks"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    roster_id = db.Column(db.Integer)
    draft_id = db.Column(db.Text)
    picked_by = db.Column(db.Text, db.ForeignKey('managers.user_id'))
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    position = db.Column(db.String)
    team = db.Column(db.String)
    amount = db.Column(db.String)

    manager = db.relationship('Manager')


class Roster(db.Model):
    __tablename__ = "rosters"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    owner_id = db.Column(db.Text, db.ForeignKey(
        'managers.user_id'), unique=True)
    wins = db.Column(db.Integer)
    losses = db.Column(db.Integer)
    ppts = db.Column(db.Integer)
    fpts = db.Column(db.Integer)
    fpts_against = db.Column(db.Integer)
    streak = db.Column(db.Text)
    record = db.Column(db.Text)
    players = db.Column(db.PickleType)

    manager = db.relationship('Manager', backref="roster")


class Player(db.Model):
    __tablename__ = "players"

    id = db.Column(db.String, primary_key=True, nullable=False)
    full_name = db.Column(db.String)
    position = db.Column(db.String)
    team = db.Column(db.String)
    age = db.Column(db.String)
    height = db.Column(db.String)
    last_name = db.Column(db.String)


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(100))
    content = db.Column(db.String(2500))
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.datetime.now())

    posted_by = db.relationship('User')

    def __repr__(self):
        return f"<Post title:{self.title} content:{self.content} created_at:{self.created_at}>"

    @property
    def friendly_datetime(self):
        """Return human readable date and time string"""

        return self.created_at.strftime("%B %d %Y, %I:%M %p")
