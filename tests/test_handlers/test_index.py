#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import tornado.web
from tornado.testing import AsyncHTTPTestCase

from sophon.handlers.index import IndexHandler


class TestHandlerIndex(AsyncHTTPTestCase):

    def get_app(self):
        return tornado.web.Application(
            [(r"/", IndexHandler)]
        )

    def test_index(self):
        response = self.fetch(r"/")
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, "Hello World!")
