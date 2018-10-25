from flask_testing import TestCase
from my_calendar import create_app
from my_calendar.database import db
from my_calendar.modules import User, Event
from datetime import datetime


class TestUser(TestCase):

    SQLALCHEMY_DATABASE_URI = "sqlite:///db_for_test.db"
    TESTING = True

    def create_app(self):
        return create_app(self)

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add_user(self):
        self.assertEqual(len(User.query.all()), 0)

        user = User.create('xua@wustl.edu', 'strong_password')
        db.session.add(user)
        db.session.commit()
        self.assertEqual(len(User.query.all()), 1)

        user = User.create('xua@sss.edu', 'strong_password')
        db.session.add(user)
        db.session.commit()
        self.assertEqual(len(User.query.all()), 2)

    def test_query_user_email(self):
        self.assertEqual(len(User.query.all()), 0)

        email, password = 'xua@wustl.edu', 'strong_password'
        user = User.create(email, password)
        user_id = user.user_id
        db.session.add(user)
        db.session.commit()
        self.assertEqual(len(User.query.all()), 1)

        query_email = User.query.filter_by(email=email).first()
        self.assertEqual(query_email.email, email)
        self.assertEqual(query_email.user_id, user_id)
        self.assertTrue(query_email.verify(password))

    def test_query_user_id(self):
        self.assertEqual(len(User.query.all()), 0)

        email, password = 'xua@wustl.edu', 'strong_password'
        user = User.create(email, password)
        user_id = user.user_id
        db.session.add(user)
        db.session.commit()
        self.assertEqual(len(User.query.all()), 1)

        query_email = User.query.filter_by(user_id=user_id).first()
        self.assertEqual(query_email.email, email)
        self.assertEqual(query_email.user_id, user_id)
        self.assertTrue(query_email.verify(password))

    def test_query_user_not_exist(self):
        self.assertIsNone(User.query.filter_by(email='this@xua').first())
        self.assertIsNone(User.query.filter_by(user_id='sdfsdf').first())

    def test_delete_user_and_events(self):
        self.assertEqual(len(User.query.all()), 0)

        user = User.create('xua@wustl.edu', 'strong_password')
        user.events = [
            Event.create('dinner', datetime.now()),
            Event.create('lunch', datetime.now()),
            Event.create('breakfast', datetime.now()),
        ]
        user_id = user.user_id
        db.session.add(user)
        db.session.commit()
        self.assertEqual(len(User.query.all()), 1)
        self.assertEqual(len(Event.query.all()), 3)

        user = User.query.filter_by(user_id=user_id).first()
        db.session.delete(user)
        db.session.commit()
        self.assertEqual(len(User.query.all()), 0)
        self.assertEqual(len(Event.query.all()), 0)
