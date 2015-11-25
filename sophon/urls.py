#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from sophon.handlers.index import IndexHandler

URL_PATTERNS = [
    (r"/", IndexHandler)
]
