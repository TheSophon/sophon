#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import subprocess


command = {
    "cpu": "top -b -n 1",
    "disk": "df -h ."
}


def get_host_status(ip):
    ret = {
        "Status": "Down",
        "CPU Load": 0,
        "Memory Usage": (0, 0),
        "Disk Usage": (0, 0)
    }
    cpu = "ansible {0} -a \"{1}\"".format(ip, command["cpu"])
    disk = "ansible {0} -a \"{1}\"".format(ip, command["disk"])
    _cpu_result = subprocess.Popen(
        cpu, shell=True, stdout=subprocess.PIPE
    ).stdout.read()
    _disk_result = subprocess.Popen(
        disk, shell=True, stdout=subprocess.PIPE
    ).stdout.read()
    cpu_result = _cpu_result.split()
    disk_result = _disk_result.split()
    if "top" in _cpu_result:
        cpu_index = cpu_result.index("average:")
        mem_index = cpu_result.index("Mem:")
        disk_index = disk_result.index("/")
        cpu_used = float(cpu_result[cpu_index + 1][:-1])
        mem_used = int(cpu_result[mem_index + 3][:-1])
        mem_not_used = int(cpu_result[mem_index + 1][:-1]) - mem_used
        disk_used = float(disk_result[disk_index - 3][:-1])
        disk_total = float(disk_result[disk_index - 4][:-1])
        if cpu_index:
            ret = {
                "Status": "Active",
                "CPU Load": cpu_used,
                "Memory Usage": (mem_used / 1024, mem_not_used / 1024),
                "Disk Usage": (disk_used, disk_total)
            }
    return ret
