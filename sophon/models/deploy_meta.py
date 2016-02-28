#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import time

from sqlalchemy import Column
from sqlalchemy.types import Integer, String, Text, PickleType

from sophon.database import BaseModel, session


# pylint: disable=too-many-instance-attributes
class DeployMeta(BaseModel):
    __tablename__ = "deploy_meta"

    id = Column(Integer, autoincrement=True, primary_key=True)
    taskname = Column(String(100), nullable=False)
    # 0: not finish, 1: successful deployment, 2: failed deployment
    user_id = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)
    created = Column(Integer, nullable=False)
    repo_uri = Column(String(100), nullable=False)
    entry_point = Column(String(100), nullable=False)
    hosts = Column(PickleType, nullable=False)
    msg = Column(Text, nullable=False)

    def __init__(self, taskname, user_id, repo_uri, entry_point, hosts):
        self.taskname = taskname
        self.user_id = user_id
        self.status = 0
        self.created = int(time.time())
        self.repo_uri = repo_uri
        self.entry_point = entry_point
        self.hosts = hosts
        self.msg = u""

    @classmethod
    def update_deploy_meta(cls, deploy_id, status, msg):
        deploy_item = cls.query.filter_by(id=deploy_id).first()
        if deploy_item:
            deploy_item.status = status
            deploy_item.msg = msg
            session.add(deploy_item)
            session.commit()
        session.close()

    @classmethod
    def get_all_deploy_summary(cls):
        deploy_items = cls.query.all()
        session.close()
        summary = dict()
        for deploy_item in deploy_items:
            summary[deploy_item.id] = {
                "Taskname": deploy_item.taskname,
                "Status": deploy_item.status,
                "Created": deploy_item.created
            }
        return summary

    @classmethod
    def get_deploy_item_by_id(cls, deploy_id):
        deploy_item = cls.query.filter_by(id=deploy_id).first()
        session.close()
        return {
            "Taskname": deploy_item.taskname,
            "Status": deploy_item.status,
            "Created": deploy_item.created,
            "Repo URI": deploy_item.repo_uri,
            "Entry Point": deploy_item.entry_point,
            "Hosts": deploy_item.hosts,
            "Msg": deploy_item.msg
        }
