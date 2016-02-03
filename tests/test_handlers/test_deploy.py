#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import json

import mock
import tornado.web
from tornado.testing import AsyncHTTPTestCase

from sophon.handlers.deploy import DeployHandler


class TestIndexHandler(AsyncHTTPTestCase):

    def get_app(self):
        return tornado.web.Application(
            [(r"/api/deploy", DeployHandler)]
        )

    @mock.patch("sophon.handlers.deploy.DeployMeta")
    @mock.patch("sophon.handlers.deploy.created2str")
    def test_get_summary(self, _created2str, _DeployMeta):
        _summary = {
            "1": {
                "Taskname": "sample_deploy",
                "Status": 0,
                "Created": 123
            }
        }
        _DeployMeta.get_all_deploy_summary.return_value = _summary
        _created2str.return_value = 345

        with mock.patch.object(
            DeployHandler, "get_secure_cookie"
        ) as _get_secure_cookie:
            _get_secure_cookie.return_value = "Alice"

            response = self.fetch(r"/api/deploy")
            response_body = json.loads(response.body)

            _summary["1"]["Created"] = 345
            _created2str.called_once_with(123)
            self.assertEqual(response_body, _summary)
