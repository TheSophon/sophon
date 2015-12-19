#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from sophon.handlers.index import IndexHandler
from sophon.handlers.user import GetUserInfoHandler, LoginHandler, LogoutHandler

URL_PATTERNS = [
    (r"/", IndexHandler),
    (r"/api/user/login", LoginHandler),
    (r"/api/user/logout", LogoutHandler),
    (r"/api/user/info", GetUserInfoHandler)
]
