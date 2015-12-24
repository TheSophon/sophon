#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from tornado.web import authenticated

from sophon.handlers import BaseHandler
from sophon.models import HostMeta


class HostStatusHandler(BaseHandler):

    @authenticated
    def get(self):
        self.write(HostMeta.get_all_hosts_status())
