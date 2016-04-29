#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from tornado.web import authenticated, HTTPError

from sophon.models import UserMeta
from sophon.database import session
from sophon.handlers import BaseHandler
from sophon.utils.new_user import new_user_public_key


class LoginHandler(BaseHandler):

    def post(self):
        username, password = (
            self.get_argument("username"), self.get_argument("password")
        )
        if username and password and UserMeta.check_password(username=username,
                                                             password=password):
            self.set_secure_cookie("username", username)
            query_data = UserMeta.query.filter_by(username=username).first()
            session.close()
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


class GetUserInfoHandler(BaseHandler):

    def get(self):
        username = self.get_secure_cookie("username")
        if username:
            query_data = UserMeta.query.filter_by(username=username).first()
            session.close()
            self.write({
                "id": query_data.id,
                "username": username,
                "type": query_data.user_type
            })
        else:
            self.write({})


class UserRegisterHandler(BaseHandler):

    @authenticated
    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")
        user_type = self.get_argument("type")
        public_key = self.get_argument("public_key")

        current_username = self.get_secure_cookie("username")
        query_data = UserMeta.query.filter_by(username=current_username).first()
        if query_data.user_type != 1:
            raise HTTPError(403)

        public_key_path = new_user_public_key(public_key)
        user = UserMeta(username=username, user_type=int(user_type),
                        password=password, public_key=public_key_path)
        session.add(user)
        session.commit()
        session.close()

        self.write({"msg": "success"})


class UserPasswordHanlder(BaseHandler):

    @authenticated
    def put(self):
        password = self.get_argument("password")
        current_username = self.get_secure_cookie("username")

        UserMeta.change_password(username=current_username, password=password)

        self.write({"msg": "success"})
