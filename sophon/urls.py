#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from sophon.handlers.index import IndexHandler
from sophon.handlers.user import GetUserInfoHandler, LoginHandler, LogoutHandler
from sophon.handlers.host import HostStatusHandler, HostProcessStatusHandler

URL_PATTERNS = [
    (r"/", IndexHandler),
    (r"/api/user/login", LoginHandler),
    (r"/api/user/logout", LogoutHandler),
    (r"/api/user/info", GetUserInfoHandler),
    (r"/api/host/status", HostStatusHandler),
    (r"/api/host/(\d+)/process_status", HostProcessStatusHandler)
]
