#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import json

from sqlalchemy import Column
from sqlalchemy.types import Integer, String, Text

from sophon.database import BaseModel


class HostMeta(BaseModel):
    __tablename__ = "host_meta"

    id = Column(Integer, autoincrement=True, primary_key=True)
    hostname = Column(String(100), nullable=False)
    ip = Column(String(40), nullable=False)
    status = Column(Text, nullable=False)
    process_status = Column(Text, nullable=False)
    supervisor_status = Column(Text, nullable=False)

    def __init__(self, hostname, ip):
        self.hostname = hostname
        self.ip = ip
        self.status = json.dumps(
            {
                "Hostname": hostname,
                "IP": ip,
                "Status": "Down",
                "CPU Load": 0,
                "Memory Usage": (0, 0),
                "Disk Usage": (0, 0)
            }
        )
        self.process_status = json.dumps({})
        self.supervisor_status = json.dumps({})

    @classmethod
    def get_all_hosts_status(cls):
        hosts = cls.query.all()
        status_list = {
            host.id: json.loads(host.status) for host in hosts
        }
        return status_list
