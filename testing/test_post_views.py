"""User View tests"""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_user_views.py


import os
from unittest import TestCase

from models import db, connect_db, User, Manager, Post
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


class PostViewsTestCase(TestCase):
    """Test views for posts"""

    def setUp(self):
        """Create test client and sample data"""

        db.drop_all()
        db.create_all()

        # Must fill managers table to create a user to create a post

        m1 = Manager(sleeper_id='724424250483650560',
                     display_name='test_name',
                     team_name='test_team')
        m2 = Manager(sleeper_id='470093099188613120',
                     display_name='test_name',
                     team_name='test_team')
        db.session.add_all([m1, m2])
        db.session.commit()

        self.client = app.test_client()

        # create a user so user can create a post
        self.testuser = User.register(sleeper_id='724424250483650560',
                                      first_name='Bojack',
                                      last_name='Horseman',
                                      email="horseman@gmail.com",
                                      password='whiskey')

        self.testuser_id = 999
        self.testuser.id = self.testuser_id
        db.session.commit()

    def test_add_post(self):
        """Test if user can add a post"""

        # Must change session because login required to make a post

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = self.testuser.id

            res = c.post(
                "/blog/new", data={"title": "test-title", "para_1": "test paragraph"})

            # Test to make sure user redirected
            self.assertEqual(res.status_code, 302)

            post = Post.query.one()
            self.assertEqual(post.title, "test-title")
            self.assertEqual(post.para_1, "test paragraph")

    def test_add_post_no_session(self):
        with self.client as c:
            res = c.post(
                "/blog/new", data={"title": "test-title", "para_1": "test paragraph"}, follow_redirects=True)

        self.assertEqual(res.status_code, 200)

        # Test to make sure post flashed explaining need for login
        self.assertIn(
            "Sorry, you must be logged in to create a blog post!", str(res.data))

    def test_add_post_invalid_user(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 12345  # This user does not exist

            res = c.post("blog/new", data={"title": "test-title",
                         "para_1": "test paragraph"}, follow_redirects=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(
                "Sorry, you must be logged in to create a blog post!", str(res.data))

    def test_post_show(self):

        p = Post(id=123, title="test title",
                 para_1="test paragraph one", para_2="test paragraph two", user_id=self.testuser.id)

        db.session.add(p)
        db.session.commit()

        with self.client as c:
            res = c.get('/blog')

            self.assertEqual(res.status_code, 200)
            self.assertIn(p.title, str(res.data))
            self.assertIn(p.para_1, str(res.data))
            self.assertIn(p.para_2, str(res.data))
            self.assertEqual(p.para_3, None)

    def test_post_delete(self):
        p = Post(id=123, title="test title", para_1="test paragraph one",
                 para_2="test paragraph two", user_id=self.testuser.id)

        db.session.add(p)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = self.testuser.id

            res = c.post('blog/123/delete', follow_redirects=True)
            self.assertEqual(res.status_code, 200)

            # Make sure the post was deleted
            p = Post.query.get(123)
            self.assertIsNone(p)

    def test_unauthorized_post_delete(self):

        # Create second user to try to delete post
        u = User.register(sleeper_id='470093099188613120',
                          first_name='Princess',
                          last_name='Caroline',
                          email="caroline@gmail.com",
                          password='testpassword')

        u.id = 456

        # Post is owned by testuser created in setUp
        p = Post(id=789, title="test title",
                 para_1="test paragraph one", user_id=self.testuser_id)

        db.session.add_all([u, p])
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 456

            res = c.post('/blog/789/delete', follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn(
                'You may only delete posts that you created!', str(res.data))

    def test_message_delete_no_authentication(self):
        p = Post(id=789, title="test title",
                 para_1="test paragraph one", user_id=self.testuser_id)

        db.session.add(p)
        db.session.commit()

        with self.client as c:
            res = c.post("/blog/789/delete", follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn(
                'Sorry, you must be logged in to delete your blog post!', str(res.data))

            # Make sure post still exists in database
            p = Post.query.get(789)
            self.assertIsNotNone(p)
