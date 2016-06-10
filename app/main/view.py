# coding=utf-8
__author__ = 'Slevin'
from . import main
from common import render_ok, render_error, make_session
from flask import request, json
from flask_restful import Api, Resource, reqparse, abort
from app.models.user import *
import jwt

api = Api(main, catch_all_404s=True)


class UserList(Resource):
    # 注册
    def post(self):
        body = json.loads(request.data)
        body['pwd'] = body['password']
        if "username" not in body:
            return render_error("please pass username ")
        if "password" not in body:
            return render_error("please pass password ")
        body.pop('password')
        result = user_create(body)
        if result == 0:
            return render_error("创建用户失败")
        res = user_get({"id": result})
        return render_ok(**{'sessionToken': make_session({'username': res[0].username})})

    # 返回所有用户
    def get(self):
        result = user_get_all()
        return render_ok(**{'user': to_users(result)})


class UserShow(Resource):
    # 修改用户信息
    def patch(self, user_id):
        body = json.loads(request.data)
        print body
        if user_id == 0:
            return render_error("please pass userid ")
        if "username" not in body:
            return render_error("please pass username ")
        if user_update(user_id, {'username': body['username']}) == 0:
            return render_error("更新失败")
        return render_ok()

    # 删除用户
    def delete(self, user_id):
        if user_id == 0:
            return render_error("please pass userid ")
        if user_delete(user_id) == 0:
            return render_error("删除失败 ")
        return render_ok()


def to_user(result):
    return {'id': result.id, 'username': result.username, 'password': result.password}


def to_users(result):
    data = []
    for i in result:
        data.append(to_user(i))
    return data


api.add_resource(UserList, '/user')
api.add_resource(UserShow, '/user/<string:user_id>')
