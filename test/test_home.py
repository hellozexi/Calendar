from flask_testing import TestCase
from flask import appcontext_pushed, g, session
from my_calendar import create_app



class TestUserApi(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite:///db_for_test.db"
    TESTING = True

    def create_app(self):
        return create_app(self)

    def test_csrf(self):
        with self.app.test_client() as client:
            respond = client.get('/')
            self.assertTrue(b'csrf_token' in respond.data)
            self.assertEqual(self.get_context_variable('csrf_token'), session['csrf_token'])
