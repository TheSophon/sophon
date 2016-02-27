#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from unittest import TestCase

import mock

from sophon.scripts.cron_tasks import (
    cron_tasks,
    cron_get_host_status
)


class TestCronGetHosttStatus(TestCase):

    @mock.patch("sophon.scripts.cron_tasks.HostMeta")
    @mock.patch("sophon.scripts.cron_tasks.get_host_status")
    def test_cron_get_host_status(self, _get_host_status, _HostMeta):
        _HostMeta.get_all_hosts_status.return_value = {
            1: {
                "Hostname": "Orion",
                "IP": "123.123.123.123",
            }
        }
        _get_host_status.return_value = {
            "Status": "Active"
        }

        cron_get_host_status()

        _HostMeta.get_all_hosts_status.assert_called_once_with()
        _HostMeta.update_host_status.assert_called_once_with(
            ip="123.123.123.123",
            status={
                "Hostname": "Orion",
                "IP": "123.123.123.123",
                "Status": "Active"
            }
        )


class TestCronTasks(TestCase):

    @mock.patch("sophon.scripts.cron_tasks.time")
    @mock.patch("sophon.scripts.cron_tasks.init_db")
    @mock.patch("sophon.scripts.cron_tasks.schedule")
    @mock.patch("sophon.scripts.cron_tasks.cron_get_host_status")
    @mock.patch("sophon.scripts.cron_tasks.SCHEDULER_JOB_PERIOD", 3)
    def test_cron_tasks(self, _cron_get_host_status, _schedule,
                        _init_db, _time):
        cron_tasks()

        _init_db.assert_called_once_with()
        _schedule.every.assert_called_once_with(3)
        _schedule.every.return_value.minutes.do.assert_called_once_with(
            _cron_get_host_status
        )
        self.assertEqual(_time.sleep.call_count, 0)
