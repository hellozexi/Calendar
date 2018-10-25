from flask import session
from flask_testing import TestCase
from my_calendar import create_app
from my_calendar.database import db
from my_calendar.modules import User


class TestUserLogout(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite:///db_for_test.db"
    TESTING = True

    def create_app(self):
        return create_app(self)

    def setUp(self):
        db.drop_all()
        db.create_all()

        self.success = {'code': 200}
        self.success_create = {'code': 201}
        self.not_json = {'code': 400, 'error': 'post type must be json'}
        self.field_not_complete = {'code': 400, 'error': 'fields not complete'}
        self.wrong_email = {'code': 400, 'error': "format check of email failed: got today's dinner"}
        self.error_need_csrf = {'code': 400, 'error': 'needs csrf token'}
        self.error_wrong_csrf = {'code': 400, 'error': 'wrong csrf token'}

        user = User.create('xua@wustl.edu', 'strong_password')
        self.user_id = user.user_id
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_logout(self):
        with self.app.test_client() as client:
            client.get('/')
            self.csrf_token = session['csrf_token']

            response = client.post('/api/users/login', json={
                'email': 'xua@wustl.edu',
                'password': 'strong_password',
                'csrf_token': self.csrf_token
                })
            self.assertEqual(response.json, self.success)
            # login check
            self.assertTrue('user_id' in session)
            self.assertEqual(session['user_id'], self.user_id)

            response = client.get('/api/users/logout')
            self.assertEqual(response.json, self.success)
            # logout check
            self.assertFalse('user_id' in session)
            self.assertTrue('csrf_token' in session)
