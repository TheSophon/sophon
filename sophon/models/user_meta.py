#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import time

from passlib.hash import pbkdf2_sha256  # pylint: disable=no-name-in-module
from sqlalchemy import Column
from sqlalchemy.types import Integer, SmallInteger, String

from sophon.database import BaseModel, session


class UserMeta(BaseModel):
    __tablename__ = "user_meta"

    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String(100), nullable=False)
    created = Column(Integer, nullable=False)
    # For user_type, 1 represent ops, 2 represent dev
    user_type = Column(SmallInteger, nullable=False)
    password = Column(String(100), nullable=False)
    public_key = Column(String(100), nullable=False)

    def __init__(self, username, user_type, password, public_key):
        self.username = username
        self.created = int(time.time())
        self.user_type = user_type
        self.password = pbkdf2_sha256.encrypt(password)
        self.public_key = public_key

    @classmethod
    def check_password(cls, username, password):
        user_mata_info = cls.query.filter_by(username=username).first()
        session.close()
        if user_mata_info:
            return pbkdf2_sha256.verify(password, user_mata_info.password)
        else:
            return False

    @classmethod
    def change_password(cls, username, password):
        user_mata_info = cls.query.filter_by(username=username).first()
        user_mata_info.password = pbkdf2_sha256.encrypt(password)
        session.add(user_mata_info)
        session.commit()
        session.close()
