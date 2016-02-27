#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy.types import Integer

from sophon.database import BaseModel, session
from sophon.models import HostMeta


class SSHPermissionMeta(BaseModel):
    __tablename__ = "ssh_permission_meta"

    id = Column(Integer, autoincrement=True, primary_key=True)
    host_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)

    def __init__(self, host_id, user_id):
        self.host_id = host_id
        self.user_id = user_id

    @classmethod
    def get_ssh_permission_by_user_id(cls, user_id):
        all_hosts_status = HostMeta.get_all_hosts_status()
        session.close()
        hosts_has_permission = set([
            item.host_id for item in cls.query.filter_by(user_id=user_id).all()
        ])
        result = {}
        for host_id in all_hosts_status.keys():
            result[host_id] = {
                "Hostname": all_hosts_status[host_id]["Hostname"],
                "IP": all_hosts_status[host_id]["IP"],
                "Has Permission": (
                    True if host_id in hosts_has_permission else False
                )
            }
        return result
