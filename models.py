from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = 'users'

    # user.id must be set to the unique sleeper ID
    id = db.Column(db.Text, primary_key=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)

    @classmethod
    def register(cls, id, first_name, last_name, email, password):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(password)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        user = cls(
            id=id,
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


class Member(db.Model):
    __tablename__ = 'members'
    user_id = db.Column(db.Text, primary_key=True, nullable=False)
    display_name = db.Column(db.Text)
    avatar_id = db.Column(db.Text)
    team_name = db.Column(db.Text)


class Roster(db.Model):
    __tablename__ = "rosters"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    owner_id = db.Column(db.Text, db.ForeignKey('members.user_id'))
    wins = db.Column(db.Integer)
    losses = db.Column(db.Integer)
    fpts = db.Column(db.Integer)
    fpts_against = db.Column(db.Integer)
    streak = db.Column(db.Text)
    record = db.Column(db.Text)


class Pick(db.Model):
    __tablename__ = "picks"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    roster_id = db.Column(db.Integer)
    draft_id = db.Column(db.Text)
    picked_by = db.Column(db.Text, db.ForeignKey('members.user_id'))
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    position = db.Column(db.String)
    team = db.Column(db.String)
    amount = db.Column(db.String)

    member = db.relationship('Member')


class Player(db.Model):
    __tablename__ = "players"

    id = db.Column(db.String, primary_key=True, nullable=False)
    full_name = db.Column(db.String)
    position = db.Column(db.String)
    team = db.Column(db.String)
    age = db.Column(db.String)
    height = db.Column(db.String)
