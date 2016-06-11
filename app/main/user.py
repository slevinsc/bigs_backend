# coding=utf-8
__author__ = 'Slevin'
from . import main
from common import render_ok, render_error, make_session, check_login, body
from flask import request, json
from flask_restful import Api, Resource
from app.models import user
from werkzeug.security import generate_password_hash

api = Api(main, catch_all_404s=True)


class UserList(Resource):
    # 注册
    def post(self):
        params = body["params"]
        params['pwd'] = params['password']
        if "username" not in params:
            return render_error("please pass username ")
        if "password" not in params:
            return render_error("please pass password ")
        params.pop('password')
        result = user.user_create(params)
        if result == 0:
            return render_error("创建用户失败")
        res = user.user_get_obj({"id": result})
        return render_ok(**{'sessionToken': make_session({'username': res.username})})

    # 返回所有用户
    @check_login
    def get(self):
        result = user.user_get_all()
        return render_ok(**{'user': _to_users(result)})


class UserLogin(Resource):
    # 登陆
    def post(self):
        params = body["params"]
        if "username" not in params:
            return render_error("please pass username ")
        if "password" not in params:
            return render_error("please pass password ")
        # print params['username']
        res = user.user_get_obj({"username": params['username']})
        # print res.username
        if res is None:
            return render_error("用户名不正确")
        if res.veify_password(params['password']) is False:
            return render_error("密码不正确")
        return render_ok(**{'sessionToken': make_session({'username': params['username']})})


class UserLogout(Resource):
    @check_login
    def delete(self):
        return render_ok()


class UserShow(Resource):
    # 修改用户信息
    @check_login
    def patch(self, user_id):
        params = body["params"]
        if user_id == 0:
            return render_error("please pass userid ")
        if "username" not in body:
            return render_error("please pass username ")
        if user.user_update(user_id, {'username': params['username']}) == 0:
            return render_error("更新失败")
        return render_ok()

    # 删除用户
    @check_login
    def delete(self, user_id):
        if user_id == 0:
            return render_error("please pass userid ")
        if user.user_delete(user_id) == 0:
            return render_error("删除失败 ")
        return render_ok()


def _to_user(result):
    return {'id': result.id, 'username': result.username, 'password': result.password}


def _to_users(result):
    data = []
    for i in result:
        data.append(_to_user(i))
    return data


api.add_resource(UserList, '/user')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(UserShow, '/user/<string:user_id>')
