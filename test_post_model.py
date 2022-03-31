"""Post model tests."""

# run these tests command line: python -m unittest test_user_model.py #

from multiprocessing.sharedctypes import Value
import os
from unittest import TestCase
from models import db, User, Post, Manager
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


class PostModelTestCase(TestCase):
    """Test post model."""

    def setUp(self):
        """Set up sample data to save to self"""
        db.drop_all()
        db.create_all()

        # Add data to manager table for foreign key connection

        m = Manager(sleeper_id='724424250483650560',
                    display_name='test_name',
                    team_name='test_team')
        db.session.add(m)
        db.session.commit()

        self.client = app.test_client()

        u = User.register(sleeper_id='724424250483650560',
                          first_name='Bojack',
                          last_name='Horseman',
                          email="horseman@gmail.com",
                          password='whiskey')
        self.uid = 33
        u.id = self.uid
        db.session.commit()

        self.u = User.query.get(self.uid)

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_post_model(self):
        """Test basic post model"""

        p = Post(user_id=self.uid, title="test post title",
                 para_1="test paragraph one")

        db.session.add(p)
        db.session.commit()

        self.assertEqual(len(self.u.posts), 1)
        self.assertEqual(self.u.posts[0].title, "test post title")
        self.assertEqual(self.u.posts[0].para_1, "test paragraph one")

    def test_invalid_post_title(self):
        """Test invalid post title"""

        p = Post(user_id=self.uid, title=None, para_1="test paragraph one")

        db.session.add(p)

        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_invalid_post_paragraph(self):
        """Test invalid post paragraph"""

        p = Post(user_id=self.uid, title="test title", para_1=None)

        db.session.add(p)

        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()
