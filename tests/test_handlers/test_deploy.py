#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import json
import urllib

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

    @mock.patch("sophon.handlers.deploy.session")
    @mock.patch("sophon.handlers.deploy.UserMeta")
    @mock.patch("sophon.handlers.deploy.DeployMeta")
    def test_new_deploy(self, _DeployMeta, _UserMeta, _session):
        _filter_by, _first = mock.Mock(), mock.Mock()
        user_item, deploy_item = mock.Mock(), mock.Mock()
        user_item.id = 42
        _UserMeta.query.filter_by.return_value = _filter_by
        _filter_by.return_value = _first
        _first.return_value = user_item
        _DeployMeta.return_value = deploy_item

        with mock.patch.object(
            DeployHandler, "get_secure_cookie"
        ) as _get_secure_cookie:
            _get_secure_cookie.return_value = "Alice"
            request_body = {
                "taskname": "sampledeploy",
                "repo_uri": "uri",
                "entry_point": "sample",
                "hosts": "[1, 2]"
            }

            response = self.fetch(
                r"/api/deploy",
                method="POST",
                body=urllib.urlencode(request_body),
                headers={
                    "Content-Type": "application/x-www-form-urlencoded"
                }
            )

            response_body = json.loads(response.body)
            self.assertEqual(response_body, {"msg": "success"})
            _DeployMeta.called_once_with(taskname="sampledeploy", user_id=42,
                                         repo_uri="uri", entry_point="sample",
                                         hosts=[1, 2])
            _session.add.called_once_with(deploy_item)
            _session.commit.called_once_with()
