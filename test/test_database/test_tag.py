from flask_testing import TestCase
from datetime import datetime
from sqlalchemy import and_, extract
from my_calendar import create_app
from my_calendar.database import db
from my_calendar.modules import User, Event, Tag


class TestTag(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite:///db_for_test.db"
    TESTING = True

    def create_app(self):
        return create_app(self)

    def setUp(self):
        db.create_all()

        user = User.create('xua@wustl.edu', 'strong_password')
        user2 = User.create('json@wustl.edu', 'strong_password')
        event = Event.create('dinner', datetime(2018, 7, 5, 18, 30, 0))
        event2 = Event.create('dinner', datetime(2018, 7, 5, 18, 30, 0))
        user.events.append(event)
        user2.events.append(event2)
        self.user_id = user.user_id
        self.user_id2 = user2.user_id
        self.event_id = event.event_id
        self.event_id2 = event2.event_id
        db.session.add(user)
        db.session.add(user2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add_tag(self):
        user = User.query.filter_by(user_id=self.user_id).first()
        user2 = User.query.filter_by(user_id=self.user_id2).first()
        event = Event.query.with_parent(user).filter_by(event_id=self.event_id).first()
        event2 = Event.query.with_parent(user2).filter_by(event_id=self.event_id2).first()
        tag = Tag(tag_name='important', activated=False)
        tag2 = Tag(tag_name='important', activated=False)
        event.tags.append(tag)
        event2.tags.append(tag2)
        db.session.commit()

        user = User.query.filter_by(user_id=self.user_id).first()
        event = Event.query.with_parent(user).filter_by(event_id=self.event_id).first()
        tags = Tag.query.with_parent(event).all()

        self.assertEqual(len(tags), 1)
        self.assertEqual(tags[0].event_id, self.event_id)
        self.assertEqual(tags[0].tag_name, 'important')

    def test_delete_cascade(self):
        user = User.query.filter_by(user_id=self.user_id).first()
        event = Event.query.with_parent(user).filter_by(event_id=self.event_id).first()
        event.tags.append(Tag(tag_name='important', activated=False))
        event.tags.append(Tag(tag_name='personal', activated=False))
        db.session.commit()
        # print(Tag.query.with_parent(event).all())
        self.assertEqual(len(Tag.query.all()), 2)

        user = User.query.filter_by(user_id=self.user_id).first()
        event = Event.query.with_parent(user).filter_by(event_id=self.event_id).first()
        db.session.delete(event)
        db.session.commit()
        self.assertEqual(len(Tag.query.all()), 0)
