#!/usr/bin/env python
# coding=utf-8


from .. import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __table__name = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.Text())

    @property
    def pwd(self):
        raise AttributeError('password is not a readable attribute')
        # return self.password

    @pwd.setter
    def pwd(self, pwd):
        self.password = generate_password_hash(pwd)

    def veify_password(self, pwd):
        return check_password_hash(self.password, pwd)

    def __repr__(self):
        return '<User %r>' % self.username


# insert
def user_create(values):
    try:
        user = User(**values)
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        print e
        return 0
    return user.id


def user_get_all():
    return db.session.query(User).all()


# select
def user_get(values):
    return User.query.filter_by(**values).all()


# update
def user_update(user_id, values):
    try:
        db.session.query(User).filter(User.id == user_id).update(values)
        db.session.commit()
    except Exception as e:
        print e
        return 0
    return 1


# delete
def user_delete(userid):
    try:
        user = User.query.get(userid)
        db.session.delete(user)
        db.session.commit()
    except Exception as e:
        print e
        return 0
    return 1
