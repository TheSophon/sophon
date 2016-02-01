#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import json

from tornado.web import authenticated

from sophon.handlers import BaseHandler
from sophon.models import HostMeta


class HostStatusHandler(BaseHandler):

    @authenticated
    def get(self):
        self.write(HostMeta.get_all_hosts_status())


class HostProcessStatusHandler(BaseHandler):

    @authenticated
    def get(self, host_id):
        self.write(
            json.dumps(HostMeta.get_host_process_status(host_id=host_id))
        )

class HostDockerStatusHandler(BaseHandler):

    @authenticated
    def get(self):
        self.write(
            json.dumps(HostMeta.get_all_hosts_dockers_status())
        )
