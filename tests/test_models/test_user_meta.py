#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from unittest import TestCase

import mock
from passlib.hash import pbkdf2_sha256  # pylint: disable=no-name-in-module

from sophon.models import UserMeta
from tests.test_models.conftest import mysql_fixture


class TestUserMeta(TestCase):

    @mysql_fixture
    def test_insert(self, session):
        _insert_data = UserMeta(username="Alice", user_type=1,
                                password="badpasswd",
                                public_key="/path/key1.pub")
        session.add(_insert_data)

        _query_data = session.query(UserMeta).filter_by(
            username="Alice"
        ).first()
        self.assertEqual(_query_data.username, "Alice")
        self.assertEqual(_query_data.user_type, 1)
        self.assertEqual(_query_data.public_key, "/path/key1.pub")
        self.assertTrue(
            pbkdf2_sha256.verify("badpasswd", _query_data.password)
        )

    @mysql_fixture
    def test_check_password_if_has_user(self, session):
        _insert_data = UserMeta(username="Bob", user_type=2,
                                password="chkpasswd",
                                public_key="/path/key2.pub")
        session.add(_insert_data)

        with mock.patch.object(
            UserMeta, "query", session.query_property()
        ) as _query:
            self.assertTrue(
                UserMeta.check_password("Bob", "chkpasswd")
            )

    @mysql_fixture
    def test_check_password_if_not_has_user(self, session):
        with mock.patch.object(
            UserMeta, "query", session.query_property()
        ) as _query:
            self.assertFalse(
                UserMeta.check_password("Bob", "chkpasswd")
            )

    @mock.patch("sophon.models.user_meta.session")
    def test_change_password(self, _session):
        sample_user = mock.Mock()

        with mock.patch.object(
            UserMeta, "query", _session.query_property()
        ) as _query:
            _query.filter_by.return_value.first.return_value = sample_user

            UserMeta.change_password("Bob", "changedpassword")

            pbkdf2_sha256.verify("changedpassword", sample_user.password)
            _session.add.assert_called_once_with(sample_user)
            _session.commit.assert_called_once_with()
            _session.close.assert_called_once_with()
