#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import json

from tornado.web import authenticated

from sophon.models import HostMeta
from sophon.handlers import BaseHandler
from sophon.database import session
from sophon.utils.new_host import new_host


class HostStatusHandler(BaseHandler):

    @authenticated
    def get(self):
        self.write(HostMeta.get_all_hosts_status())


class HostProcessStatusHandler(BaseHandler):

    @authenticated
    def get(self, host_id):
        self.write(
            json.dumps(HostMeta.get_host_process_status(host_id=int(host_id)))
        )


class HostDockerStatusHandler(BaseHandler):

    @authenticated
    def get(self):
        self.write(
            json.dumps(HostMeta.get_all_hosts_dockers_status())
        )


class HostHandler(BaseHandler):

    @authenticated
    def post(self):
        hostname = self.get_argument("hostname")
        ip = self.get_argument("ip")
        ssh_secret_key = self.get_argument("ssh_secret_key")

        new_host(ip=ip, ssh_secret_key=ssh_secret_key)

        _host_item = HostMeta(hostname=hostname, ip=ip)
        session.add(_host_item)
        session.commit()
        session.close()


        self.write({
            _host_item.id: json.loads(_host_item.status)
        })
