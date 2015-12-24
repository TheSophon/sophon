#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import json
from unittest import TestCase

import mock

from sophon.models import HostMeta
from tests.test_models.conftest import mysql_fixture


class TestHostMeta(TestCase):

    @mysql_fixture
    def test_insert(self, session):
        _insert_data = HostMeta(hostname="Marvin", ip="123.456.78.9")
        session.add(_insert_data)

        _query_data = session.query(HostMeta).filter_by(
            hostname="Marvin"
        ).first()
        self.assertEqual(_query_data.hostname, "Marvin")
        self.assertEqual(_query_data.ip, "123.456.78.9")
        self.assertEqual(_query_data.status, json.dumps(
            {
                "Hostname": "Marvin",
                "IP": "123.456.78.9",
                "Status": "Down",
                "CPU Load": 0,
                "Memory Usage": (0, 0),
                "Disk Usage": (0, 0)
            }
        ))

        self.assertEqual(_query_data.process_status, json.dumps({}))
        self.assertEqual(_query_data.supervisor_status, json.dumps({}))

    @mysql_fixture
    def test_get_all_hosts_status(self, session):
        _insert_data = HostMeta(hostname="Marvin", ip="123.456.78.9")
        session.add(_insert_data)

        with mock.patch.object(
            HostMeta, "query", session.query_property()
        ) as _query:
            hosts_status = HostMeta.get_all_hosts_status()
            self.assertEqual(hosts_status, {
                1: {
                    "Hostname": "Marvin",
                    "IP": "123.456.78.9",
                    "Status": "Down",
                    "CPU Load": 0,
                    "Memory Usage": [0, 0],
                    "Disk Usage": [0, 0]
                }
            })
