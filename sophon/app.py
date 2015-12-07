#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import tornado.httpserver
import tornado.ioloop
import tornado.web

from sophon.config import TORNADO_SETTINGS
from sophon.urls import URL_PATTERNS


def main():
    application = tornado.web.Application(
        URL_PATTERNS, **TORNADO_SETTINGS
    )
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()
