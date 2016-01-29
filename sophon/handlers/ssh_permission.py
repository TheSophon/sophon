#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import subprocess

from tornado.web import authenticated

from sophon.database import session
from sophon.handlers import BaseHandler
from sophon.models import HostMeta, UserMeta, SSHPermissionMeta


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
        user_item = UserMeta.query.filter_by(username=username).first()
        user_id, public_key_path = user_item.id, user_item.public_key
        host_id, has_permission = (
            int(self.get_argument("host_id")),
            True if self.get_argument("has_permission") == "true" else False
        )
        if has_permission:
            host_ip = HostMeta.get_all_hosts_status()[host_id]["IP"]
            ssh_permission_item = SSHPermissionMeta(
                user_id=user_id, host_id=host_id
            )
            session.add(ssh_permission_item)
            session.commit()

            print public_key_path, user_id

            subprocess.call(
                "cat " + public_key_path + " | ssh root@" + host_ip +
                " \'cat >> ~/.ssh/authorized_keys\'", shell=True
            )
        self.write({"msg": "success"})
