#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from unittest import TestCase

import mock

from sophon.utils.new_host import new_host


class TestNewDeploy(TestCase):

    SSH_CONFIG_TEMPLATE = "{ip} - {key_filename}"

    @mock.patch("__builtin__.open")
    @mock.patch("sophon.utils.new_host.os")
    @mock.patch("sophon.utils.new_host.uuid")
    @mock.patch("sophon.utils.new_host.SSH_CONFIG_TEMPLATE",
                SSH_CONFIG_TEMPLATE)
    def test_new_deploy(self, _uuid, _os, _open):
        _os.path.expanduser.return_value = "/home/user"
        _os.path.join.side_effect = [
            "/home/user/.ssh/key_filename",
            "/home/user/.ssh/config"
        ]
        _uuid.uuid1 = mock.Mock()
        _uuid.uuid1.return_value = "sampleuuid"
        _key_file, _ssh_config_file, _inventory_file = (
            mock.MagicMock(spec=file),
            mock.MagicMock(spec=file),
            mock.MagicMock(spec=file),
        )

        def open_side_effect(*args):
            arg2file = {
                "/home/user/.ssh/key_filename": _key_file,
                "/home/user/.ssh/config": _ssh_config_file,
                "./hosts": _inventory_file
            }
            return arg2file[args[0]]

        _open.side_effect = open_side_effect

        new_host(ip="123.456.78.9", ssh_secret_key="sample_secret_key")

        _os.path.expanduser.assert_called_once_with("~")
        _uuid.uuid1.assert_called_once_with()
        self.assertEqual(
            _os.path.join.call_args_list,
            [
                mock.call("/home/user", ".ssh", "sampleuuid"),
                mock.call("/home/user", ".ssh", "config")
            ]
        )
        _key_file.__enter__.return_value.write.assert_called_once_with(
            "sample_secret_key\r\n"
        )
        _os.chmod.assert_called_once_with("/home/user/.ssh/key_filename", 0o600)
        _ssh_config_file.__enter__.return_value.write.assert_called_once_with(
            self.SSH_CONFIG_TEMPLATE.format(
                ip="123.456.78.9",
                key_filename="/home/user/.ssh/key_filename"
            )
        )
        _inventory_file.__enter__.return_value.write.assert_called_once_with(
            "123.456.78.9\r\n"
        )
