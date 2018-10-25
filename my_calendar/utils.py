from functools import wraps
from flask import g, Response, request, session
from uuid import uuid4
from datetime import datetime
from dateutil import parser
import json
import re


re_email = re.compile(r"^[0-9A-Za-z\.]*@[A-Za-z\.]*$")
re_word = re.compile(r'^[\w\s]*$')


def check_email(email: str) -> bool:
    return re_email.match(email) is not None


def check_word(word: str) -> bool:
    return re_word.match(word) is not None


def check_datetime(d: str) -> bool:
    date = None
    try:
        date = parser.parse(d)
    except ValueError:
        return False
    finally:
        if date is None:
            return False
        return type(date) is datetime


def get_weekday(date: datetime) -> int:
    return int(date.strftime('%w'))


def check_exist_fields(*args):
    """
    return True if one of them in the dict
    return False only all of them are not in dict
    """
    def actual_check(value) -> bool:
        if type(value) is not dict:
            return False
        flag = False
        for arg in args:
            if arg in value:
                flag = True
        return flag
    return actual_check


def new_uuid() -> str:
    return str(uuid4()).replace('-', '')


def json_response(d: dict) -> Response:
    return Response(json.dumps(d), mimetype='application/json')


def result_success() -> Response:
    return json_response({'code': 200})


def result_create_success() -> Response:
    return json_response({'code': 201})


def error_msg(code: int, msg: str) -> Response:
    return json_response({
        'code': code,
        'error': msg
    })


def need_login(func):
    @wraps(func)
    def return_func(*args, **kwargs):
        if g.user is None:
            return error_msg(403, 'need to login')
        return func(*args, **kwargs)
    return return_func


def need_csrf(func):
    @wraps(func)
    def return_func(*args, **kwargs):
        json_content = request.json
        if json_content is None:
            return error_msg(400, 'post type must be json')
        if 'csrf_token' not in json_content:
            return error_msg(400, 'needs csrf token')
        if g.csrf_token is None:
            return error_msg(404, 'missing csrf token in session')
        if json_content['csrf_token'] != g.csrf_token:
            return error_msg(400, 'wrong csrf token')
        return func(*args, **kwargs)
    return return_func


def check_fields(*fields):
    def actual_decorator(func):
        @wraps(func)
        def wrapper_check_fields(*args, **kwargs):
            json_content = request.json
            if json_content is None:
                return error_msg(400, 'post type must be json')
            for (field, field_type, check_function) in fields:
                if field not in json_content:
                    return error_msg(400, 'fields not complete')
                value = json_content[field]
                if type(value) is not field_type:
                    return error_msg(400, f'error type of {field}: expect {field_type} but get {type(value)}')
                if not check_function(value):
                    return error_msg(400, f'format check of {field} failed: got {value}')
            return func(*args, **kwargs)
        return wrapper_check_fields
    return actual_decorator
