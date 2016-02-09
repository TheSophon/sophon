#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import json

import mock
import tornado.web
from tornado.testing import AsyncHTTPTestCase

from sophon.config import TORNADO_SETTINGS
from sophon.handlers.host import (
    HostStatusHandler, HostProcessStatusHandler, HostDockerStatusHandler
)


class TestHostStatusHandler(AsyncHTTPTestCase):

    def get_app(self):
        return tornado.web.Application(
            [(r"/api/host/status", HostStatusHandler)],
            **TORNADO_SETTINGS
        )

    @mock.patch("sophon.handlers.host.HostMeta")
    def test_get_all_hosts_status(self, _HostMeta):
        host_status = {
            "1": {
                "Status": "Active",
                "CPU Load": 0.2,
                "Memory Usage": [2000, 4000],
                "IP": "192.168.1.10",
                "Hostname": "Orion",
                "Disk Usage": [20, 40]
            }
        }
        _HostMeta.get_all_hosts_status.return_value = host_status

        with mock.patch.object(
            HostStatusHandler, "get_secure_cookie"
        ) as _get_secure_cookie:
            _get_secure_cookie.return_value = "Alice"

            response = self.fetch("/api/host/status")
            response_body = json.loads(response.body)

            self.assertEqual(response.code, 200)
            self.assertEqual(response_body, host_status)
            _HostMeta.get_all_hosts_status.assert_called_once_with()


class TestHostProcessStatusHandler(AsyncHTTPTestCase):

    def get_app(self):
        return tornado.web.Application(
            [(r"/api/host/(\d+)/process_status", HostProcessStatusHandler)],
            **TORNADO_SETTINGS
        )

    @mock.patch("sophon.handlers.host.HostMeta")
    def test_get_host_process_status(self, _HostMeta):
        host_process_status = [
            {
                "PID": 1,
                "User": "root",
                "Memory Usage": 0.1,
                "CPU Usage": 0.2,
                "Time": "11:11:11",
                "Command": "/bin/place/holder"
            },
            {
                "PID": 2,
                "User": "toor",
                "Memory Usage": 0.2,
                "CPU Usage": 0.4,
                "Time": "23:33:33",
                "Command": "/bin/another/place/holder"
            }
        ]
        _HostMeta.get_host_process_status.return_value = host_process_status

        with mock.patch.object(
            HostProcessStatusHandler, "get_secure_cookie"
        ) as _get_secure_cookie:
            _get_secure_cookie.return_value = "Alice"

            response = self.fetch("/api/host/1/process_status")
            response_body = json.loads(response.body)

            self.assertEqual(response.code, 200)
            self.assertEqual(response_body, host_process_status)
            _HostMeta.get_host_process_status.assert_called_once_with(
                host_id=1
            )


class TestHostDockerStatusHandler(AsyncHTTPTestCase):

    def get_app(self):
        return tornado.web.Application(
            [(r"/api/host/dockers_status", HostDockerStatusHandler)],
            **TORNADO_SETTINGS
        )

    @mock.patch("sophon.handlers.host.HostMeta")
    def test_get_all_hosts_docker_status(self, _HostMeta):
        _docker_status = [
            {
                "Container ID": "4c01dxxb339c",
                "Image": "ubuntu:12.04",
            }
        ]
        _HostMeta.get_all_hosts_dockers_status.return_value = _docker_status

        with mock.patch.object(
            HostDockerStatusHandler, "get_secure_cookie"
        ) as _get_secure_cookie:
            _get_secure_cookie.return_value = "Alice"

            response = self.fetch("/api/host/dockers_status")
            response_body = json.loads(response.body)

            self.assertEqual(response.code, 200)
            self.assertEqual(response_body, _docker_status)
            _HostMeta.get_all_hosts_dockers_status.assert_called_once_with()
