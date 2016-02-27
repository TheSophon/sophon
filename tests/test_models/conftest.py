#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from functools import wraps

from sqlalchemy.orm import scoped_session

from sophon.database import db_session, engine, init_db


def mysql_fixture(func):
    """Fixture for SQLAlchemy Session
    """
    @wraps(func)
    def fixed_func(self, *args, **kwargs):
        init_db()
        connection = engine.connect()
        transaction = connection.begin()
        session = scoped_session(db_session)

        fixed_args = tuple(list(args) + [session])

        try:
            func(self, *fixed_args, **kwargs)
        finally:
            session.remove()
            session.close()
            transaction.rollback()
            connection.close()

    return fixed_func
