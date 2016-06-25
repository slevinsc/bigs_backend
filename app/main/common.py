#!/usr/bin/env python
# coding=utf-8
import hashlib
import jwt

from flask import jsonify, current_app, request, json

from .. import redis_store

body = {}
session = {}


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


def make_sign(**kwargs):
    params = sorted(kwargs.iteritems(), lambda asd: asd[0])
    sign_tmp = []
    for k in params:
        if k is not "sign":
            sign_tmp.append(k + "=" + params[k])
    sign = "&".join(sign_tmp)
    sign = sign + "key=" + current_app.config.get('SIGN_KEY')
    print sign
    m2 = hashlib.md5()
    m2.update(sign)
    return m2.hexdigest().lower()


def get_params():
    try:
        body['params'] = json.loads(request.data)
    except Exception as e:
        print e
        return render_error("JSON格式不对")


def check_sign(func):
    def sign(*args, **kw):
        params = body['params']
        if 'sign' not in params:
            return render_error("没找到sign参数")
        s = make_sign(params)
        if s != params['sign']:
            return render_error("sign认证不通过")
        return func(*args, **kw)

    return sign


def check_login(func):
    def get_session(*args, **kw):
        params = body['params']
        if 'sessionToken' not in params:
            return render_error("您未登陆或者会话已过期")
        try:
            key = jwt.decode(params['sessionToken'], current_app.config.get('SECRET_KEY'), algorithms=['HS256'])
            value = redis_store.get(key['username'])
        except Exception as e:
            print e
            return render_error("获取session失败")
        session['username'] = key['username']
        if value != params['sessionToken']:
            return render_error("非法用户")
        return func(*args, **kw)

    return get_session


def del_session():
    redis_store.delete(session['username'])
