from flask_testing import TestCase
from datetime import datetime
from sqlalchemy import and_, extract
from my_calendar import create_app
from my_calendar.database import db
from my_calendar.modules import User, Event


class TestEvnet(TestCase):

    SQLALCHEMY_DATABASE_URI = "sqlite:///db_for_test.db"
    TESTING = True

    def create_app(self):
        return create_app(self)

    def setUp(self):
        db.create_all()

        user = User.create('xua@wustl.edu', 'strong_password')
        self.user_id = user.user_id
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add_event(self):
        user = User.query.filter_by(user_id=self.user_id).first()
        event = Event.create('dinner', datetime(2018, 6, 5, 18, 30, 0))
        user.events.append(event)
        db.session.commit()

        user = User.query.filter_by(user_id=self.user_id).first()
        self.assertEqual(len(Event.query.with_parent(user).all()), 1)
        self.assertIs(type(Event.query.with_parent(user).all()), list)

    def test_add_events(self):
        user = User.query.filter_by(user_id=self.user_id).first()
        user.events = [
            Event.create('dinner', datetime(2018, 6, 5, 18, 30, 0)),
            Event.create('dinner', datetime(2018, 6, 6, 18, 30, 0)),
            Event.create('dinner', datetime(2018, 6, 7, 18, 30, 0)),
            Event.create('dinner', datetime(2018, 6, 8, 18, 30, 0))
        ]
        db.session.commit()
        user = User.query.filter_by(user_id=self.user_id).first()
        self.assertEqual(len(Event.query.with_parent(user).all()), 4)
        self.assertIs(type(Event.query.with_parent(user).all()), list)

        user = User.query.filter_by(user_id=self.user_id).first()
        user.events += [
            Event.create('dinner', datetime(2018, 7, 5, 18, 30, 0)),
            Event.create('dinner', datetime(2018, 7, 6, 18, 30, 0)),
            Event.create('dinner', datetime(2018, 7, 7, 18, 30, 0)),
            Event.create('dinner', datetime(2018, 7, 8, 18, 30, 0))
        ]
        self.assertEqual(len(Event.query.with_parent(user).all()), 8)
        self.assertIs(type(Event.query.with_parent(user).all()), list)

    def test_query_event(self):
        user = User.query.filter_by(user_id=self.user_id).first()
        event_name, event_time = 'dinner', datetime(2018, 6, 5, 18, 30, 0)
        event = Event.create(event_name, event_time)
        event_id = event.event_id
        user.events.append(event)
        db.session.commit()

        user = User.query.filter_by(user_id=self.user_id).first()
        query_event = Event.query.with_parent(user).filter_by(event_id=event_id).first()
        self.assertEqual(query_event.event_id, event_id)
        self.assertEqual(query_event.event_name, event_name)
        self.assertEqual(query_event.event_time, event_time)

    def test_year_month_query(self):
        month_6 = [
            Event.create('dinner', datetime(2018, 6, 5, 18, 30, 0)),
            Event.create('dinner', datetime(2018, 6, 6, 18, 30, 0)),
            Event.create('dinner', datetime(2018, 6, 7, 18, 30, 0)),
            Event.create('dinner', datetime(2018, 6, 8, 18, 30, 0))
        ]
        month_7 = [
            Event.create('dinner', datetime(2018, 7, 5, 18, 30, 0)),
            Event.create('dinner', datetime(2018, 7, 6, 18, 30, 0)),
            Event.create('dinner', datetime(2018, 7, 7, 18, 30, 0)),
            Event.create('dinner', datetime(2018, 7, 8, 18, 30, 0))
        ]

        event_id6 = set([event.event_id for event in month_6])

        user = User.query.filter_by(user_id=self.user_id).first()
        user.events += month_6
        user.events += month_7
        db.session.commit()

        self.assertEqual(len(Event.query.with_parent(user).all()), 8)
        user = User.query.filter_by(user_id=self.user_id).first()
        events = Event.query.with_parent(user).filter(and_(
            extract('year', Event.event_time) == 2018,
            extract('month', Event.event_time) == 6,
        )).all()

        self.assertEqual(len(events), 4)
        self.assertSetEqual(event_id6, set([event.event_id for event in events]))

    def test_modify(self):
        user = User.query.filter_by(user_id=self.user_id).first()
        event_name, event_time = 'dinner', datetime(2018, 6, 5, 18, 30, 0)
        another_event, another_time = 'lunch', datetime(2018, 10, 7, 18, 30, 0)
        event = Event.create(event_name, event_time)
        event_id = event.event_id
        user.events.append(event)
        db.session.commit()

        user = User.query.filter_by(user_id=self.user_id).first()
        query_event = Event.query.with_parent(user).filter_by(event_id=event_id).first()
        query_event.event_name = another_event
        db.session.commit()

        user = User.query.filter_by(user_id=self.user_id).first()
        query_event = Event.query.with_parent(user).filter_by(event_id=event_id).first()
        self.assertEqual(query_event.event_name, another_event)

        user = User.query.filter_by(user_id=self.user_id).first()
        query_event = Event.query.with_parent(user).filter_by(event_id=event_id).first()
        query_event.event_time = another_time
        db.session.commit()

        user = User.query.filter_by(user_id=self.user_id).first()
        query_event = Event.query.with_parent(user).filter_by(event_id=event_id).first()
        self.assertEqual(query_event.event_time, another_time)

    def test_delete(self):
        user = User.query.filter_by(user_id=self.user_id).first()
        self.assertEqual(len(Event.query.with_parent(user).all()), 0)

        event_name, event_time = 'dinner', datetime(2018, 6, 5, 18, 30, 0)
        event = Event.create(event_name, event_time)
        event_id = event.event_id
        user.events.append(event)
        db.session.commit()

        self.assertEqual(len(Event.query.with_parent(user).all()), 1)

        query_event = Event.query.with_parent(user).filter_by(event_id=event_id).first()
        db.session.delete(query_event)
        db.session.commit()

        self.assertEqual(len(Event.query.with_parent(user).all()), 0)
