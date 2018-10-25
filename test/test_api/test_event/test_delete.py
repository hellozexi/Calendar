from flask import session
from flask_testing import TestCase
from datetime import datetime
from my_calendar import create_app
from my_calendar.database import db
from my_calendar.modules import User, Event, Tag


class TestEventDelete(TestCase):
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
        self.error_need_login = {'code': 403, 'error': 'need to login'}
        self.error_need_csrf = {'code': 400, 'error': 'needs csrf token'}
        self.error_wrong_csrf = {'code': 400, 'error': 'wrong csrf token'}

        user = User.create('xua@wustl.edu', 'strong_password')
        another_user = User.create('jason@wustl.edu', 'strong_password')
        event = Event.create('dinner', datetime(2017, 7, 7, 18, 30, 0))
        another_event = Event.create('lunch', datetime(2017, 7, 7, 18, 30, 0))
        self.user_id = user.user_id
        self.event_id = event.event_id
        self.another_user_id = another_user.user_id
        self.another_event_id = another_event.event_id
        user.events.append(event)
        another_user.events.append(another_event)
        db.session.add(user)
        db.session.add(another_user)
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

    def test_delete_event(self):
        with self.app.test_client() as client:
            self.login(client)

            user = User.query.filter_by(user_id=self.user_id).first()
            user.events += [
                Event.create('dinner', datetime(2018, 6, 5, 18, 30, 0)),
                Event.create('dinner', datetime(2018, 6, 6, 18, 30, 0)),
                Event.create('dinner', datetime(2018, 6, 7, 18, 30, 0)),
                Event.create('dinner', datetime(2018, 6, 8, 18, 30, 0)),
            ]
            event_id = user.events[0].event_id
            self.assertEqual(len(Event.query.with_parent(user).all()), 5)
            db.session.commit()

            response = client.post('/api/events/delete', json={
                'event_id': event_id,
                'csrf_token': self.csrf_token
            })
            user = User.query.filter_by(user_id=self.user_id).first()
            self.assertEqual(response.json, self.success)
            self.assertEqual(len(Event.query.with_parent(user).all()), 4)
