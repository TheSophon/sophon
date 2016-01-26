#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from sophon.config import SQLALCHEMY_DATABASE_URI

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
db_session = sessionmaker(bind=engine)
session = scoped_session(db_session)
BaseModel = declarative_base()
BaseModel.query = session.query_property()


def init_db():
    BaseModel.metadata.create_all(bind=engine)

def drop_db():
    BaseModel.metadata.drop_all(bind=engine)

from sophon.models import HostMeta  # pylint: disable=unused-import, wrong-import-position
from sophon.models import UserMeta  # pylint: disable=unused-import, wrong-import-position
from sophon.models import SSHPermissionMeta  # pylint: disable=unused-import, wrong-import-position
