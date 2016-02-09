#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import json
import urllib

import mock
import tornado.web
from tornado.testing import AsyncHTTPTestCase

from sophon.config import TORNADO_SETTINGS
from sophon.handlers.deploy import DeployHandler, DeployDetailHandler


class TestDeployHandler(AsyncHTTPTestCase):

    def get_app(self):
        return tornado.web.Application(
            [(r"/api/deploy", DeployHandler)],
            **TORNADO_SETTINGS
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
            _created2str.assert_called_once_with(123)
            self.assertEqual(response_body, _summary)

    @mock.patch("sophon.handlers.deploy.session")
    @mock.patch("sophon.handlers.deploy.do_deploy")
    @mock.patch("sophon.handlers.deploy.UserMeta")
    @mock.patch("sophon.handlers.deploy.DeployMeta")
    @mock.patch("sophon.handlers.deploy.created2str")
    def test_new_deploy(self, _created2str, _DeployMeta, _UserMeta,
                        _do_deploy, _session):
        _filter_by, user_item, deploy_item = (
            mock.Mock(), mock.Mock(), mock.Mock()
        )
        user_item.id = 42
        deploy_item.id, deploy_item.taskname = 66, "sampledeploy"
        deploy_item.status, deploy_item.created = 0, 77
        _UserMeta.query.filter_by.return_value = _filter_by
        _filter_by.first.return_value = user_item
        _DeployMeta.return_value = deploy_item
        _created2str.return_value = "sampletime"

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
            self.assertEqual(
                response_body,
                {
                    "66": {
                        "Taskname": "sampledeploy",
                        "Status": 0,
                        "Created": "sampletime"
                    }
                }
            )
            _created2str.assert_called_once_with(created=77)
            _DeployMeta.assert_called_once_with(taskname="sampledeploy",
                                                user_id=42,
                                                repo_uri="uri",
                                                entry_point="sample",
                                                hosts=[1, 2])
            _session.add.assert_called_once_with(deploy_item)
            _session.commit.assert_called_once_with()
            _do_deploy.assert_called_once_with(deploy_id=66, user="root",
                                               entry_point="sample",
                                               hosts=[1, 2], repo_uri="uri")


class TestDeployDetailHandler(AsyncHTTPTestCase):

    def get_app(self):
        return tornado.web.Application(
            [(r"/api/deploy/(\d+)", DeployDetailHandler)],
            **TORNADO_SETTINGS
        )

    @mock.patch("sophon.handlers.deploy.DeployMeta")
    @mock.patch("sophon.handlers.deploy.created2str")
    def test_get_deploy_detail(self, _created2str, _DeployMeta):
        _DeployMeta.get_deploy_item_by_id.return_value = {
            "Taskname": "sample_task",
            "Created": 123
        }
        _created2str.return_value = 456

        with mock.patch.object(
            DeployDetailHandler, "get_secure_cookie"
        ) as _get_secure_cookie:
            _get_secure_cookie.return_value = "Alice"
            response = self.fetch(r"/api/deploy/42")

            response_body = json.loads(response.body)
            self.assertEqual(
                response_body,
                {
                    "Taskname": "sample_task",
                    "Created": 456
                }
            )
            _DeployMeta.get_deploy_item_by_id.assert_called_once_with(
                deploy_id=42
            )
            _created2str.assert_called_once_with(created=123)
