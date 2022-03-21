from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

import requests

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String, primary_key=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, nullable=False)
    avatar_id = db.Column(db.Text)

    @classmethod
    def register(cls, id, first_name, last_name, email, password):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(password)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # Make API call to sleeper to get 'username' and 'avatar'
        user_data = requests.get(
            f"https://api.sleeper.app/v1/user/{id}").json()

        user = cls(
            id=id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_utf8,
            username=user_data['username'],
            avatar_id=user_data['avatar']
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


class Roster(db.Model):
    __tablename__ = "rosters"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    owner_id = db.Column(db.String, db.ForeignKey('users.id'))
    wins = db.Column(db.Integer)
    losses = db.Column(db.Integer)
    fpts = db.Column(db.Integer)
    fpts_against = db.Column(db.Integer)
    streak = db.Column(db.Text)
    record = db.Column(db.Text)


class Player(db.Model):
    __tablename_ = "players"

    id = db.Column(db.String, primary_key=True, nullable=False)
    full_name = db.Column(db.String)
    position = db.Column(db.String)
    team = db.Column(db.String)
    age = db.Column(db.String)
    height = db.Column(db.String)
