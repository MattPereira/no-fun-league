"""User View tests"""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_user_views.py


import os
from unittest import TestCase

from models import db, connect_db, User, Manager
from sleeper import update_managers


# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgres:///no-fun-league-test"

# Now we can import app
from app import app


db.create_all()


app.config['WTF_CSRF_ENABLED'] = False


class UserViewsTestCase(TestCase):
    """Test views for users"""

    def setUp(self):
        """Create test client and sample data"""

        db.drop_all()
        db.create_all()

        # Must fill the managers table because users table has not nullable foreign key pointing to managers.sleeper_id
        update_managers()

        self.client = app.test_client()

        # Must use valid sleeper_id for registering a user because user model has foreign key pointing to manager model

        self.testuser = User.register(sleeper_id='724424250483650560', first_name='Bojack',
                                      last_name='Horseman', email="horseman@gmail.com", password='whiskey')
        self.testuser_id = 777
        self.testuser.id = self.testuser_id

        db.session.commit()

    def teardown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp

    def test_user_show(self):
        """Tests if user profile is displayed properly"""
        with self.client as c:
            res = c.get(f"/managers/{self.testuser_id}")

            self.assertEqual(res.status_code, 200)

            self.assertIn('Bojack', str(res.data))
            self.assertIn('Manager of', str(res.data))
            self.assertIn('Team Philosophy', str(res.data))

    def test_show_user_edit_form(self):
        """Tests if user edit form is displayed properly"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = self.testuser_id

            res = c.get(f'/managers/{self.testuser_id}/update')

            self.assertEqual(res.status_code, 200)

            self.assertIn('Edit Profile', str(res.data))
            self.assertIn('First Name', str(res.data))
            self.assertIn('Email', str(res.data))
            self.assertIn('SAVE', str(res.data))

    def test_show_user_edit_form_no_session(self):
        """Tests to make sure access denied and redirected to 401.html if no 'user_id' in session"""
        with self.client as c:

            res = c.get(f'/managers/{self.testuser_id}/update')

            self.assertEqual(res.status_code, 200)
            self.assertIn(
                'You must be logged in to access this route!', str(res.data))

    def test_edit_user(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = self.testuser_id

            data = {
                "first_name": "Princess",
                "last_name": "Caroline",
                "email": "caroline@gmail.com",
                "location": 'hollywood, CA',
                "bio": "test bio",
                "philosophy": "test philosophy",
                "fav_team": "cin",
                "fav_position": "WR",
                "fav_player": "1111",
                "trade_desire": "4"
            }

            res = c.post(
                f'/managers/{self.testuser_id}/update', data=data, follow_redirects=True)

            self.assertEqual(res.status_code, 200)

            self.assertNotIn("Bojack", str(res.data))
            self.assertNotIn("Horseman", str(res.data))
            self.assertNotIn("Horseman@gmail.com", str(res.data))

            self.assertIn("Princess", str(res.data))
            self.assertIn("Caroline", str(res.data))
            self.assertIn("test bio", str(res.data))
            self.assertIn("test philosophy", str(res.data))
            self.assertIn("cin", str(res.data))
            self.assertIn("WR", str(res.data))

    def test_edit_user_no_session(self):
        """Tests to make sure unauthorized and redirected to 401.html if no 'user_id' in session"""
        with self.client as c:

            data = {
                "first_name": "Princess",
                "last_name": "Caroline",
                "email": "caroline@gmail.com",
                "location": 'hollywood, CA',
                "bio": "test bio",
                "philosophy": "test philosophy",
                "fav_team": "cin",
                "fav_position": "WR",
                "fav_player": "1111",
                "trade_desire": "4"
            }

            res = c.post(f'/managers/{self.testuser_id}/update', data=data)

            self.assertEqual(res.status_code, 200)
            self.assertIn(
                'You must be logged in to access this route!', str(res.data))
