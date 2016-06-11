#!/usr/bin/env python
# coding=utf-8

from flask import jsonify, current_app, request, json
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
    redis_store.set(payload['username'], token, 3600)
    return token


def check_login(func):
    def get_session(*args, **kw):
        body = json.loads(request.data)
        if 'sessionToken' not in body:
            return render_error("您未登陆或者会话已过期")
        try:
            key = jwt.decode(body['sessionToken'], current_app.config.get('SECRET_KEY'), algorithms=['HS256'])
            value = redis_store.get(key['username'])
        except Exception as e:
            print e
            return render_error("获取session失败")
        if value != body['sessionToken']:
            return render_error("非法用户")
        return func(*args, **kw)

    return get_session
