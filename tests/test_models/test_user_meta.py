#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from unittest import TestCase

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
    def test_check_password(self, session):
        _insert_data = UserMeta(username="Bob", user_type=2,
                                password="chkpasswd",
                                public_key="/path/key2.pub")
        session.add(_insert_data)

        _query_data = session.query(UserMeta).filter_by(username="Bob").first()
        self.assertTrue(
            pbkdf2_sha256.verify("chkpasswd", _query_data.password)
        )

