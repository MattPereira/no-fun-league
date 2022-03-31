from unittest import TestCase
from app import app


app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class NoFunLeagueViews(TestCase):

    def test_home_page(self):
        """Make sure home page is displayed"""
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('The No Fun League', html)
            self.assertIn('League Blog', html)
            self.assertIn('2021 Champion', html)

    def test_drafts(self):
        """Make sure draft board page is displayed"""
        with app.test_client() as client:
            res = client.get('/draftboard')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('2021 DRAFTBOARD', html)

    def test_blog(self):
        """Make sure blog page is displayed"""
        with app.test_client() as client:
            res = client.get('/blog')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('The No Fun League Blog', html)
            self.assertIn('NEW POST', html)

    def test_polls(self):
        """Make sure polls page is displayed"""
        with app.test_client() as client:
            res = client.get('/polls')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('The No Fun League Polls', html)
            self.assertIn('NEW PROPOSAL', html)
