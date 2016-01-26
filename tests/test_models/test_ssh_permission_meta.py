#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from unittest import TestCase

import mock

from sophon.models import SSHPermissionMeta
from tests.test_models.conftest import mysql_fixture


class TestSSHPermssionMeta(TestCase):

    @mysql_fixture
    def test_insert(self, session):
        _insert_data = SSHPermissionMeta(user_id=1, host_id=2)
        session.add(_insert_data)

        _query_datas = session.query(SSHPermissionMeta).filter_by(
            user_id=1
        ).all()

        self.assertEqual(len(_query_datas), 1)
        self.assertEqual(_query_datas[0].user_id, 1)
        self.assertEqual(_query_datas[0].host_id, 2)

    @mysql_fixture
    @mock.patch("sophon.models.ssh_permission_meta.HostMeta")
    def test_get_host_process_status(self, session, _HostMeta):
        _insert_data = SSHPermissionMeta(user_id=1, host_id=2)
        session.add(_insert_data)
        _HostMeta.get_all_hosts_status.return_value = {
            1: {
                "Hostname": "Marvin",
                "IP": "123.456.78.9"
            },
            2: {
                "Hostname": "Bob",
                "IP": "132.654.87.9"
            }
        }

        with mock.patch.object(
            SSHPermissionMeta, "query", session.query_property()
        ) as _query:
            ssh_permission_items = (
                SSHPermissionMeta.get_ssh_permission_by_user_id(user_id=1)
            )
            self.assertEqual(ssh_permission_items, {
                1: {
                    "Hostname": "Marvin",
                    "IP": "123.456.78.9",
                    "Has Permission": False
                },
                2: {
                    "Hostname": "Bob",
                    "IP": "132.654.87.9",
                    "Has Permission": True
                }
            })
