from flask.blueprints import Blueprint
from flask import session, g, request, Response
from sqlalchemy import and_, extract
from dateutil import parser
from .database import db
from .modules import User, Event, Tag
from .utils import (
    need_login, error_msg, json_response, need_csrf,
    check_fields, check_email, check_word, check_datetime, check_exist_fields,
    result_success, result_create_success
)


bp_api = Blueprint('api', __name__, url_prefix='/api')


@bp_api.before_app_request
def load_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(user_id=user_id).first()

    csrf_token = session.get('csrf_token')
    if csrf_token is None:
        g.csrf_token = None
    else:
        g.csrf_token = csrf_token


@bp_api.route('/users/login', methods=['POST'])
@need_csrf
@check_fields(('email', str, check_email), ('password', str, check_word))
def login():
    content = request.json
    email, password = content['email'], content['password']
    user = User.query.filter_by(email=email).first()
    if user is None:
        return error_msg(404, 'user not exist')
    if not user.verify(password):
        return error_msg(403, 'wrong password')
    session['user_id'] = user.user_id
    return result_success()


@bp_api.route('/users/register', methods=['POST'])
@need_csrf
@check_fields(('email', str, check_email), ('password', str, check_word))
def register():
    content = request.json
    email, password = content['email'], content['password']
    # check if exist same user
    if User.query.filter_by(email=email).first() is not None:
        return error_msg(403, 'user already exist')
    user = User.create(email, password)
    db.session.add(user)
    db.session.commit()
    return result_create_success()


@bp_api.route('/users/logout', methods=['GET'])
# @need_login
def logout():
    session.clear()
    if g.csrf_token is not None:
        session['csrf_token'] = g.csrf_token
    return result_success()


@bp_api.route('/users/delete', methods=['POST'])
@need_csrf
@need_login
def user_delete():
    # check if exist same user
    db.session.delete(g.user)
    db.session.commit()
    session.clear()
    if g.csrf_token is not None:
        session['csrf_token'] = g.csrf_token
    return result_success()


@bp_api.route('/events/user', methods=['POST'])
@need_csrf
@need_login
@check_fields(('year', int, lambda y: True), ('month', int, lambda m: 0 <= m <= 11))
def get_user_events():
    content = request.json
    year, month = int(content['year']), int(content['month'])
    events = Event.query.with_parent(g.user).filter(and_(
        extract('year', Event.event_time) == year,
        extract('month', Event.event_time) == month,
    )).all()
    return json_response({
        'code': 200,
        'events': [event.to_dict() for event in events]
    })


@bp_api.route('/events/create', methods=['POST'])
@need_csrf
@need_login
@check_fields(('event_name', str, check_word),
              ('event_time', str, check_datetime))
def create_events():
    content = request.json
    event_name, event_time = content['event_name'], parser.parse(content['event_time'])
    event = Event.create(event_name=event_name, event_time=event_time)
    g.user.events.append(event)
    db.session.commit()
    return result_create_success()


@bp_api.route('/events/update', methods=['POST'])
@need_csrf
@need_login
@check_fields(('event_id', str, check_word),
              ('update_fields', dict, check_exist_fields('event_name', 'event_time')))
def update_events():
    content = request.json
    event_id, update_fields = content['event_id'], content['update_fields']
    event = Event.query.with_parent(g.user).filter_by(event_id=event_id).first()
    if event is None:
        return error_msg(404, 'event not exist')
    if 'event_name' in update_fields:
        event_name = update_fields['event_name']
        if check_word(event_name):
            event.event_name = event_name
        else:
            return error_msg(403, 'event_name format is invalid')
    if 'event_time' in update_fields:
        event_time = update_fields['event_time']
        if check_datetime(event_time):
            event.event_time = parser.parse(event_time)
        else:
            return error_msg(403, 'event_time format is invalid')
    db.session.commit()
    return result_success()


@bp_api.route('/events/delete', methods=['POST'])
@need_csrf
@need_login
@check_fields(('event_id', str, check_word))
def delete_event():
    content = request.json
    event_id = content['event_id']
    event = Event.query.with_parent(g.user).filter_by(event_id=event_id).first()
    if event is None:
        return error_msg(404, 'event not exist')
    db.session.delete(event)
    db.session.commit()
    return result_success()


@bp_api.route('/tags/create', methods=['POST'])
@need_login
@need_csrf
@check_fields(('event_id', str, check_word), ('tag_name', str, check_word))
def create_tag():
    content = request.json
    event_id, tag_name = content['event_id'], content['tag_name']
    event = Event.query.with_parent(g.user).filter_by(event_id=event_id).first()
    if event is None:
        return error_msg(404, 'event not exist')
    if 'activated' in content and type(content['activated']) is bool:
        activated = content['activated']
    else:
        activated = False
    if Tag.query.with_parent(event).filter_by(tag_name=tag_name).first() is not None:
        return error_msg(400, 'tag already exist')
    tag = Tag(tag_name=tag_name, activated=activated)
    event.tags.append(tag)
    db.session.commit()
    return result_create_success()


@bp_api.route('/tags/event', methods=['POST'])
@need_csrf
@need_login
@check_fields(('event_id', str, check_word))
def get_tags():
    content = request.json
    event_id = content['event_id']
    event = Event.query.with_parent(g.user).filter_by(event_id=event_id).first()
    if event is None:
        return error_msg(404, 'event not exist')
    return json_response({
        'code': 200,
        'tags': [tag.to_dict() for tag in event.tags]
    })


@bp_api.route('/tags/update', methods=['POST'])
@need_csrf
@need_login
@check_fields(('event_id', str, check_word), ('tag_name', str, check_word), ('activated', bool, lambda x: True))
def update_tag():
    content = request.json
    event_id, tag_name, activated = content['event_id'], content['tag_name'], content['activated']
    event = Event.query.with_parent(g.user).filter_by(event_id=event_id).first()
    if event is None:
        return error_msg(404, 'event not exist')
    tag = Tag.query.with_parent(event).filter_by(tag_name=tag_name).first()
    if tag is None:
        return error_msg(404, 'tag not exist')
    tag.activated = activated
    db.session.commit()
    return result_success()


@bp_api.route('/tags/delete', methods=['POST'])
@need_csrf
@need_login
@check_fields(('event_id', str, check_word), ('tag_name', str, check_word))
def delete_tag():
    content = request.json
    event_id, tag_name = content['event_id'], content['tag_name']
    event = Event.query.with_parent(g.user).filter_by(event_id=event_id).first()
    if event is None:
        return error_msg(404, 'event not exist')
    tag = Tag.query.with_parent(event).filter_by(tag_name=tag_name).first()
    if tag is None:
        return error_msg(404, 'tag not exist')
    db.session.delete(tag)
    db.session.commit()
    return result_success()
