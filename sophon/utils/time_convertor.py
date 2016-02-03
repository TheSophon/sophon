#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import time


def created2str(created):
    _time = time.localtime(created)
    return time.strftime("%d %b %Y %H:%M:%S", _time)
