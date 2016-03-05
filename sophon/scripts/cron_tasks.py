#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import time

import schedule

from sophon.database import init_db
from sophon.models import HostMeta
from sophon.config import SCHEDULER_JOB_PERIOD
from sophon.utils.status import get_host_status, get_host_process_status


def cron_get_host_status():
    hosts_status = HostMeta.get_all_hosts_status()
    for host_id in hosts_status:
        host_ip = hosts_status[host_id]["IP"]
        host_status = get_host_status(host_ip)
        host_status.update(
            {
                "Hostname": hosts_status[host_id]["Hostname"],
                "IP": hosts_status[host_id]["IP"]
            }
        )
        HostMeta.update_host_status(ip=host_ip, status=host_status)


def cron_get_host_process_status():
    hosts_status = HostMeta.get_all_hosts_status()
    for host_id in hosts_status:
        host_ip = hosts_status[host_id]["IP"]
        process_status = get_host_process_status(host_ip)
        HostMeta.update_host_process_status(ip=host_ip,
                                            process_status=process_status)


def cron_tasks():
    init_db()
    schedule.every(SCHEDULER_JOB_PERIOD).minutes.do(cron_get_host_status)
    schedule.every(SCHEDULER_JOB_PERIOD).minutes.do(
        cron_get_host_process_status
    )
    while schedule.run_pending() is None:
        time.sleep(1)
