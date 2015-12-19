#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from sophon.models import UserMeta
from sophon.handlers import BaseHandler


class LoginHandler(BaseHandler):

    def post(self):
        username, password = (
            self.get_argument("username"), self.get_argument("password")
        )
        if UserMeta.check_password(username=username,
                                   password=password):
            self.set_secure_cookie("username", username)
            query_data = UserMeta.query.filter_by(username=username).first()
            self.write({
                "id": query_data.id,
                "username": username,
                "type": query_data.user_type
            })
        else:
            self.write({
                "msg": "Wrong username or password"
            })


class LogoutHandler(BaseHandler):

    def get(self):
        self.clear_cookie("username")
        self.write({})


class GetUserHandler(BaseHandler):

    def get(self):
        username = self.get_secure_cookie("username")
        if username:
            query_data = UserMeta.query.filter_by(username=username).first()
            self.write({
                "id": query_data.id,
                "username": username,
                "type": query_data.user_type
            })
        else:
            self.write({})
