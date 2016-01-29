#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import json
import urllib

import mock
import tornado.web
from tornado.testing import AsyncHTTPTestCase

from sophon.handlers.ssh_permission import SSHPermissionHandler


class TestSSHPermissionHandler(AsyncHTTPTestCase):

    def get_app(self):
        return tornado.web.Application(
            [(r"/api/host/ssh_permission", SSHPermissionHandler)]
        )

    @mock.patch("sophon.handlers.ssh_permission.UserMeta")
    @mock.patch("sophon.handlers.ssh_permission.SSHPermissionMeta")
    def test_get_ssh_permissions(self, _SSHPermissionMeta, _UserMeta):
        _user_item, _filter_by = mock.Mock(), mock.Mock()
        _UserMeta.query.filter_by.return_value = _filter_by
        _filter_by.return_value, _user_item.id = _user_item, 42
        ssh_permissions = {
            1: {
                "Hostname": "GLaDos",
                "IP": "123.456.78.9",
                "Has Permission": False
            },
            2: {
                "Hostname": "Alice",
                "IP": "132.654.87.9",
                "Has Permission": True
            }
        }
        _SSHPermissionMeta.get_ssh_permission_by_user_id.return_value = (
            ssh_permissions
        )

        with mock.patch.object(
            SSHPermissionHandler, "get_secure_cookie"
        ) as _get_secure_cookie:
            _get_secure_cookie.return_value = "Alice"

            response = self.fetch(r"/api/host/ssh_permission")
            response_body = json.loads(response.body)

            self.assertEqual(response.code, 200)
            self.assertEqual(
                response_body,
                {str(key): val for key, val in ssh_permissions.items()}
            )
            _SSHPermissionMeta.get_ssh_permission_by_user_id.called_once_with(
                user_id=42
            )

    @mock.patch("sophon.handlers.ssh_permission.subprocess")
    @mock.patch("sophon.handlers.ssh_permission.HostMeta")
    @mock.patch("sophon.handlers.ssh_permission.UserMeta")
    @mock.patch("sophon.handlers.ssh_permission.session")
    @mock.patch("sophon.handlers.ssh_permission.SSHPermissionMeta")
    def test_update_ssh_permissions(self, _SSHPermissionMeta,
                                    _session, _UserMeta,
                                    _HostMeta, _subprocess):
        _ssh_permission_item, _user_item, _filter_by = (
            mock.Mock(), mock.Mock(), mock.Mock()
        )
        _UserMeta.query.filter_by.return_value = _filter_by
        _filter_by.first.return_value = _user_item
        _user_item.id, _user_item.public_key = 42, "/path/key.pub"
        _SSHPermissionMeta.return_value = _ssh_permission_item
        _HostMeta.get_all_hosts_status.return_value = {
            24: {"IP": "123.456.78.9"}
        }

        with mock.patch.object(
            SSHPermissionHandler, "get_secure_cookie"
        ) as _get_secure_cookie:
            _get_secure_cookie.return_value = "Alice"

            request_body = {
                "host_id": 24,
                "has_permission": "true"
            }
            response = self.fetch(
                r"/api/host/ssh_permission",
                method="PATCH",
                body=urllib.urlencode(request_body),
                headers={
                    "Content-Type": "application/x-www-form-urlencoded"
                }
            )
            response_body = json.loads(response.body)

            _SSHPermissionMeta.called_once_with(
                user_id=42, host_id=24
            )
            _HostMeta.get_all_hosts_status.called_once_with()
            _session.add.called_once_with(_ssh_permission_item)
            _session.commit.called_once_with()
            self.assertEqual(response.code, 200)
            self.assertEqual(response_body, {"msg": "success"})
            _subprocess.call.called_once_with(
                "cat /path/key.pub | ssh root@123.456.78.9" +
                " \'cat >> ~/.ssh/authorized_keys\'"
                , shell=True
            )
