#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import time

from passlib.hash import pbkdf2_sha256  # pylint: disable=no-name-in-module
from sqlalchemy import Column
from sqlalchemy.types import Integer, SmallInteger, String

from sophon.database import BaseModel


class UserMeta(BaseModel):
    __tablename__ = "user_meta"

    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String(100), nullable=False)
    created = Column(Integer, nullable=False)
    # For user_type, 1 represent dev, 2 represent ops
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
        return pbkdf2_sha256.verify(password, user_mata_info.password)
