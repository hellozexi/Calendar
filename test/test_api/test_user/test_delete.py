from flask import session
from flask_testing import TestCase
from datetime import datetime
from my_calendar import create_app
from my_calendar.database import db
from my_calendar.modules import User, Event


class TestUserDelete(TestCase):
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
        self.error_need_login = {'code': 403, 'error': 'need to login'}
        self.error_need_csrf = {'code': 400, 'error': 'needs csrf token'}
        self.error_wrong_csrf = {'code': 400, 'error': 'wrong csrf token'}

        user = User.create('xua@wustl.edu', 'strong_password')
        self.user_id = user.user_id
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def login(self, client):
        client.get('/')
        self.csrf_token = session['csrf_token']

        response = client.post('/api/users/login', json={
            'email': 'xua@wustl.edu',
            'password': 'strong_password',
            'csrf_token': self.csrf_token
        })
        self.assertEqual(response.json, self.success)

    def test_delete(self):
        with self.app.test_client() as client:
            self.login(client)

            response = client.post('/api/users/delete', json={
                'csrf_token': self.csrf_token
            })
            self.assertEqual(response.json, self.success)
            # logout check
            self.assertFalse('user_id' in session)
            self.assertTrue('csrf_token' in session)

            self.assertEqual(len(User.query.all()), 0)
            self.assertIsNone(User.query.filter_by(user_id=self.user_id).first())

    def test_delete_with_events(self):
        with self.app.test_client() as client:
            self.login(client)

            user = User.query.filter_by(user_id=self.user_id).first()
            user.events = [
                Event.create('dinner', datetime.now()),
                Event.create('lunch', datetime.now()),
                Event.create('breakfast', datetime.now()),
            ]
            db.session.commit()
            self.assertEqual(len(User.query.all()), 1)
            self.assertEqual(len(Event.query.all()), 3)

            response = client.post('/api/users/delete', json={
                'csrf_token': self.csrf_token
            })
            self.assertEqual(response.json, self.success)
            # logout check
            self.assertFalse('user_id' in session)
            self.assertTrue('csrf_token' in session)

            self.assertEqual(len(User.query.all()), 0)
            self.assertEqual(len(Event.query.all()), 0)
            self.assertIsNone(User.query.filter_by(user_id=self.user_id).first())

    def test_without_login(self):
        with self.app.test_client() as client:
            client.get('/')
            self.csrf_token = session['csrf_token']

            response = client.post('/api/users/delete', json={
                'csrf_token': self.csrf_token
            })
            self.assertEqual(response.json, self.error_need_login)
            self.assertEqual(len(User.query.all()), 1)
            self.assertIsNotNone(User.query.filter_by(user_id=self.user_id).first())

    def test_without_csrf(self):
        self.assertEqual(len(User.query.all()), 1)
        with self.app.test_client() as client:
            client.get('/')
            self.csrf_token = session['csrf_token']

            response = client.post('/api/users/delete', json={
                # 'csrf_token': self.csrf_token
            })
            self.assertEqual(response.json, self.error_need_csrf)
            self.assertEqual(len(User.query.all()), 1)
            self.assertIsNotNone(User.query.filter_by(user_id=self.user_id).first())

    def test_wrong_csrf(self):
        self.assertEqual(len(User.query.all()), 1)
        with self.app.test_client() as client:
            client.get('/')
            self.csrf_token = session['csrf_token']

            response = client.post('/api/users/delete', json={
                'csrf_token': 'not csrf'
            })
            self.assertEqual(response.json, self.error_wrong_csrf)
            self.assertEqual(len(User.query.all()), 1)
            self.assertIsNotNone(User.query.filter_by(user_id=self.user_id).first())