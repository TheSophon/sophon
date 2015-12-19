#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import tornado.web
from tornado.testing import AsyncHTTPTestCase

from sophon.config import TORNADO_SETTINGS
from sophon.urls import URL_PATTERNS


class TestApp(AsyncHTTPTestCase):

    def get_app(self):
        return tornado.web.Application(
            URL_PATTERNS, **TORNADO_SETTINGS
        )

    def test_app(self):
        response = self.fetch(r"/")
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, "Hello World!")
