#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import tornado.httpserver
import tornado.ioloop
import tornado.web

from sophon.config import TORNADO_SETTINGS, LISTEN_ADDR
from sophon.database import init_db
from sophon.urls import URL_PATTERNS


def main():
    init_db()
    application = tornado.web.Application(
        URL_PATTERNS, **TORNADO_SETTINGS
    )
    application.listen(8888, address=LISTEN_ADDR)
    tornado.ioloop.IOLoop.current().start()
