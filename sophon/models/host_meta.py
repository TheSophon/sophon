#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import json

from sqlalchemy import Column
from sqlalchemy.types import Integer, String, Text

from sophon.database import BaseModel, session


class HostMeta(BaseModel):
    __tablename__ = "host_meta"

    id = Column(Integer, autoincrement=True, primary_key=True)
    hostname = Column(String(100), nullable=False)
    ip = Column(String(40), nullable=False)
    status = Column(Text, nullable=False)
    process_status = Column(Text, nullable=False)
    dockers_status = Column(Text, nullable=False)

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
        self.process_status = json.dumps([])
        self.dockers_status = json.dumps([])

    @classmethod
    def get_all_hosts_status(cls):
        hosts = cls.query.all()
        session.close()
        status_list = {
            host.id: json.loads(host.status) for host in hosts
        }
        return status_list

    @classmethod
    def update_host_status(cls, ip, status):
        host = cls.query.filter_by(ip=ip).first()
        session.close()
        if host:
            host.status = json.dumps(status)
            session.commit()

    @classmethod
    def get_host_process_status(cls, host_id):
        host = cls.query.filter_by(id=host_id).first()
        session.close()
        return json.loads(host.process_status) if host else {}

    @classmethod
    def update_host_process_status(cls, ip, process_status):
        host = cls.query.filter_by(ip=ip).first()
        if host:
            host.process_status = json.dumps(process_status)
            session.commit()
        session.close()

    @classmethod
    def get_all_hosts_dockers_status(cls):
        hosts = cls.query.all()
        session.close()
        result = []
        for host in hosts:
            for docker_status in json.loads(host.dockers_status):
                _docker_status = dict(docker_status)
                _docker_status.update({
                    "Hostname": host.hostname,
                    "IP": host.ip
                })
                result.append(_docker_status)
        return result

    @classmethod
    def update_host_dockers_status(cls, ip, dockers_status):
        host = cls.query.filter_by(ip=ip).first()
        if host:
            host.dockers_status = json.dumps(dockers_status)
            session.commit()
        session.close()
