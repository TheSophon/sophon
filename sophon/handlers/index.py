#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from sophon.handlers import BaseHandler


class IndexHandler(BaseHandler):

    def get(self):
        self.write("Hello World!")
