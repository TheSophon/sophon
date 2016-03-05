#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import copy
import subprocess


command = {
    "cpu": "top -b -n 1",
    "disk": "df -h .",
    "process": "top -b -n 1"
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
    cpu_result = subprocess.Popen(
        cpu, shell=True, stdout=subprocess.PIPE
    ).stdout.read().split()
    disk_result = subprocess.Popen(
        disk, shell=True, stdout=subprocess.PIPE
    ).stdout.read().split()
    if "Cpu" in "".join(cpu_result):
        cpu_index = cpu_result.index("average:")
        mem_index = cpu_result.index("Mem:")
        disk_index = disk_result.index("/")
        cpu_used = float(cpu_result[cpu_index + 1][:-1])
        mem_used = int(cpu_result[mem_index + 3].rstrip("K"))
        mem_all = int(cpu_result[mem_index + 1].rstrip("K"))
        disk_used = float(disk_result[disk_index - 3][:-1])
        disk_total = float(disk_result[disk_index - 4][:-1])
        if cpu_index:
            ret = {
                "Status": "Active",
                "CPU Load": cpu_used,
                "Memory Usage": (mem_used / 1024, mem_all / 1024),
                "Disk Usage": (disk_used, disk_total)
            }
    return ret


def get_host_process_status(ip):
    ret = {
        "PID": 0,
        "User": "none",
        "Memory Usage": 0.0,
        "CPU Usage": 0.0,
        "Time": "0:00.00",
        "Command": "sample"
    }
    process = "ansible {0} -a \"{1}\"".format(ip, command["process"])
    process_result = subprocess.Popen(
        process, shell=True, stdout=subprocess.PIPE
    ).stdout.read().split()
    result = list()
    if "COMMAND" in "".join(process_result):
        process_index = process_result.index("COMMAND")
        for x in range(0, 5):
            ret_temp = copy.deepcopy(ret)
            new_index = process_index + 12 * x
            ret_temp["PID"] = process_result[new_index + 1]
            ret_temp["User"] = process_result[new_index + 2]
            ret_temp["Memory Usage"] = process_result[new_index + 10]
            ret_temp["Time"] = process_result[new_index + 11]
            ret_temp["Command"] = process_result[new_index + 12]
            result.append(ret_temp)
    return result
