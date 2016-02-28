#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from unittest import TestCase

import mock

from sophon.utils.deploy import deploy, do_deploy


class TestDeploy(TestCase):

    @mock.patch("sophon.utils.deploy.subprocess")
    @mock.patch("sophon.utils.deploy.DeployMeta")
    def test_deploy(self, _DeloyMeta, _os):
        _popen = mock.Mock()
        _os.Popen.return_value, _popen.stdout.read.return_value = (
            _popen, "samplemsg"
        )

        deploy(deploy_id=1, entry_point="sample", user="root",
               hosts_ip=["123.45.67.89"],
               repo_uri="https://github.com/TheSophon/sophon-deploy-sample.git")

        _popen.stdout.read.assert_called_once_with()
        _DeloyMeta.update_deploy_meta.assert_called_once_with(
            deploy_id=1,
            status=1,
            msg="samplemsg"
        )

    @mock.patch("sophon.utils.deploy.deploy")
    @mock.patch("sophon.utils.deploy.Process")
    @mock.patch("sophon.utils.deploy.HostMeta")
    def test_do_deploy(self, _HostMeta, _Process, _deploy):
        _process_item = mock.Mock()
        _Process.return_value = _process_item
        _HostMeta.get_all_hosts_status.return_value = {
            1: {"IP": "123.45.67.89"}
        }

        do_deploy(1, "sample_entry_point", "root", [1], "uri")

        _HostMeta.get_all_hosts_status.assert_called_once_with()
        _Process.assert_called_once_with(
            target=_deploy,
            kwargs={
                "deploy_id": 1,
                "user": "root",
                "entry_point": "sample_entry_point",
                "hosts_ip": ["123.45.67.89"],
                "repo_uri": "uri"
            }
        )
        _process_item.start.assert_called_once_with()
