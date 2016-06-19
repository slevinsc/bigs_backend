#!/usr/bin/env python
# coding=utf-8

import unittest
from flask import json
from app import create_app, db
from app.models.user import user_create


class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        pass

    def test_register(self):
        reqJSON = json.dumps({'username': 'test', 'password': '000000'})
        reponse = self.client.post('/user', data=reqJSON)
        self.assertTrue('200' in reponse.data)
        print json.loads(reponse.data)

    def test_login(self):
        user_create({'username': 'test', 'pwd': '000000'})
        reqJSON = json.dumps({'username': 'test', 'password': '000000'})
        reponse = self.client.post('/login', data=reqJSON)
        self.assertTrue('200' in reponse.data)
        print json.loads(reponse.data)


if __name__ == '__main__':
    unittest.main()
