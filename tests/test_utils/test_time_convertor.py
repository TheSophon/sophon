#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from unittest import TestCase

import mock

from sophon.utils.time_convertor import created2str


class TestCreated2str(TestCase):

    @mock.patch("sophon.utils.time_convertor.time")
    def test_created2str(self, _time):
        _localtime = mock.Mock()
        _time.localtime.return_value = _localtime
        _time.strftime.return_value = "sample_time"

        result = created2str(123)

        _time.localtime.called_once_with()
        _time.strftime.called_once_with(
            "%d %b %Y %H:%M:%S", _localtime
        )
        self.assertEqual(result, "sample_time")
