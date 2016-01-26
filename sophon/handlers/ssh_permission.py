#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from tornado.web import authenticated

from sophon.database import session
from sophon.handlers import BaseHandler
from sophon.models import UserMeta, SSHPermissionMeta


class SSHPermissionHandler(BaseHandler):

    @authenticated
    def get(self):
        username = self.get_secure_cookie("username")
        user_id = UserMeta.query.filter_by(username=username).first().id
        self.write(
            SSHPermissionMeta.get_ssh_permission_by_user_id(user_id=user_id)
        )

    @authenticated
    def patch(self):
        username = self.get_secure_cookie("username")
        user_id = UserMeta.query.filter_by(username=username).first().id
        host_id, has_permission = (
            int(self.get_argument("host_id")),
            True if self.get_argument("has_permission") == "true" else False
        )
        if has_permission:
            ssh_permission_item = SSHPermissionMeta(
                user_id=user_id, host_id=host_id
            )
            session.add(ssh_permission_item)
            session.commit()
        self.write({"msg": "success"})
