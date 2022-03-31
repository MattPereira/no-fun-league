"""User model tests."""

# run these tests command line: python -m unittest test_user_model.py #

from multiprocessing.sharedctypes import Value
import os
from unittest import TestCase
from models import db, User
from sqlalchemy import exc
from psycopg2 import errors
from sleeper import update_managers

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database


os.environ['DATABASE_URL'] = "postgres:///no-fun-league-test"


# Now we can import app
from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test user model."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        # Easy way to fill the managers table because users table has not nullable foreign key pointing to Manager.sleeper_id
        update_managers()

        # Must use valid sleeper_id for testing

        u1 = User.register(sleeper_id='724424250483650560',
                           first_name='Bojack',
                           last_name='Horseman',
                           email="horseman@gmail.com",
                           password='whiskey')

        uid1 = 111
        u1.id = uid1

        db.session.add(u1)
        db.session.commit()

        u1 = User.query.get(uid1)

        self.u1 = u1
        self.uid1 = uid1

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_user_model(self):
        """Test user model relationship to manager model"""

        # using 'baretank' sleeper id to test relationship from user table to manager table
        u = User(
            sleeper_id='470093099188613120',
            first_name='Todd',
            last_name='Chavez',
            email="todd@gmail.com",
            password="testpassword"
        )

        db.session.add(u)
        db.session.commit()

        # User should be manager of exactly one team
        self.assertEqual(u.manager.display_name, "baretank")
        self.assertEqual(u.manager.sleeper_id, "470093099188613120")
        self.assertEqual(
            repr(u), "<User id=1 first_name=Todd last_name=Chavez>")

    def test_valid_register(self):
        """test the User.register classmethod"""

        jake = User.register('723670786174451712', 'Jake',
                             'Dame', 'jDame@gmail.com', 'joeybee')

        u_id = 777
        jake.id = u_id
        db.session.commit()

        jake = User.query.get(u_id)
        self.assertIsNotNone(jake)
        self.assertEqual(jake.sleeper_id, '723670786174451712')
        self.assertEqual(jake.email, 'jDame@gmail.com')
        self.assertNotEqual(jake.password, 'joeybee')
        # Bcrypt strings should start with $2b$
        self.assertTrue(jake.password.startswith("$2b$"))

    def test_invalid_sleeeper_id_register(self):
        """Test invalid User.sleeper_id"""

        with self.assertRaises(exc.IntegrityError) as context:
            invalid = User.register(None, 'testfirst', 'testlast',
                                    'oopsie@gmail.com', 'testpassword')
            db.session.commit()

    def test_invalid_name_register(self):
        """Test invalid User.first_name """
        with self.assertRaises(exc.IntegrityError) as context:
            invalid = User.register('723670786174451712', None, 'testlast',
                                    'oopsie@gmail.com', 'testpassword')
            db.session.commit()

    def test_invalid_email_register(self):
        """Test invalid User.email"""
        with self.assertRaises(exc.IntegrityError) as context:
            invalid = User.register('723670786174451712', 'testfirst', 'testlast',
                                    None, 'testpassword')
            db.session.commit()

    def test_invalid_password_register(self):
        """Test invalid User.password"""
        with self.assertRaises(ValueError) as context:
            invalid = User.register('723670786174451712', 'testfirst', 'testlast',
                                    'test@gmail.com', None)
            db.session.commit()

    def test_taken_sleeper_id_register(self):
        """Test trying to register with sleeper_id that is already taken"""

        u1 = User.register('723670786174451712', 'Jake',
                           'Dame', 'jDame@gmail.com', 'joeybee')
        u1_id = 999
        u1.id = u1_id
        db.session.commit()

        u2 = User.register('723670786174451712', 'Jake',
                           'Dame', 'jDame@gmail.com', 'joeybee')

        u2_id = 888
        u2.id = u2_id

        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_valid_authenticate(self):
        """Test that the user created in setUp can successfully login"""
        u = User.authenticate(self.u1.email, "whiskey")

        self.assertIsNotNone(u)
        self.assertEqual(u.id, self.uid1)

    def test_invalid_email(self):
        self.assertFalse(User.authenticate('MrRobot', "whiskey"))

    def test_wrong_password(self):
        self.assertFalse(User.authenticate(self.u1.email, "wrongpassword"))
