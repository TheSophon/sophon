#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from unittest import TestCase

import mock

from sophon.utils.new_user import new_user_public_key


class TestNewUser(TestCase):

    @mock.patch("__builtin__.open")
    @mock.patch("sophon.utils.new_user.os")
    @mock.patch("sophon.utils.new_user.uuid")
    def test_new_user_public_key(self, _uuid, _os, _open):
        _os.path.expanduser.return_value = "/home/user"
        _os.path.join.return_value = "/home/user/.ssh/public_key_filname.pub"
        _uuid.uuid1 = mock.Mock()
        _uuid.uuid1.return_value = "sampleuuid"
        _public_key_file = mock.MagicMock(spec=file)
        _open.return_value = _public_key_file

        result = new_user_public_key(ssh_public_key="sample_public_key")

        self.assertEqual(result, "/home/user/.ssh/public_key_filname.pub")
        _os.path.expanduser.assert_called_once_with("~")
        _uuid.uuid1.assert_called_once_with()
        _os.path.join.assert_called_once_with(
            "/home/user", ".ssh", "sampleuuid.pub"
        )
        _public_key_file.__enter__.return_value.write.assert_called_once_with(
            "sample_public_key\r\n"
        )
