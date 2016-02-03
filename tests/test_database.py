#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from unittest import TestCase

from sqlalchemy import create_engine, inspect

from sophon.config import SQLALCHEMY_DATABASE_URI
from sophon.database import drop_db, init_db


class TestDatabase(TestCase):

    def setUp(self):
        self.engine = create_engine(SQLALCHEMY_DATABASE_URI)
        self.inspector = inspect(self.engine)

    def test_init_db(self):
        init_db()
        table_names = self.inspector.get_table_names()
        self.assertItemsEqual(
            ["host_meta", "deploy_meta", "user_meta", "ssh_permission_meta"],
            table_names
        )

    def test_drop_db(self):
        init_db()
        drop_db()
        table_names = self.inspector.get_table_names()
        self.assertListEqual([], table_names)
