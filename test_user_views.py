"""User View tests"""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_user_views.py

from app import app
import os
from unittest import TestCase

from models import db, connect_db, User, Manager, Pick, Roster, Player, Post, Proposal, ProposalVotes


# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///no-fun-league-test"

# Now we can import app


db.create_all()


app.config['WTF_CSRF_ENABLED'] = False


class UserViewTestCase(TestCase):
    """Test views for users"""

    def setUp(self):
        """Create test client and sample data"""

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

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
        with self.client as c:
            res = c.get(f"/managers/{self.testuser_id}")

            self.assertEqual(res.status_code, 200)

            self.assertIn('Bojack', str(res.data))
