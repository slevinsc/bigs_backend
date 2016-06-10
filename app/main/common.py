#!/usr/bin/env python
# coding=utf-8

from flask import jsonify, current_app
import jwt
from .. import redis_store


def render_error(message):
    response = jsonify({
        'code': 500,
        'msg': message
    })
    response.status_code = 200
    return response


def render_ok(**kwargs):
    content = {'code': 200,
               'msg': "ok",
               }
    if kwargs:
        content['data'] = kwargs
    response = jsonify(content)
    response.status_code = 200
    return response


def make_session(payload):
    token = jwt.encode(payload, current_app.config.get('SECRET_KEY'), algorithm='HS256')
    redis_store.set(payload['username'], token, 10)
    return token


def get_session(token):
    return jwt.decode(token, current_app.config.get('SECRET_KEY'), algorithms=['HS256'])
