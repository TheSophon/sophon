#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import commands

command = {
    "cpu": "top -b -n 1",
    "disk": "df -h ."
}

def get_index(result, word):
    index = 0
    for x in result:
        index = index + 1
        if x == word:
            return index
    return 0

def get_host_status():
    ret = {
        "Status": "",
        "CPU Load": "", 
        "Memory Usage": "",
        "Disk Usage": ""
    }
    cpu = 'ansible all -a "%s"' % (command["cpu"])
    disk = 'ansible all -a "%s"' % (command["disk"])
    cpu_result = commands.getstatusoutput(cpu)
    disk_result = commands.getstatusoutput(disk)
    cpu_result = cpu_result[1].split()
    disk_result = disk_result[1].split()
    if cpu_result[2] == "FAILED":
        ret["Status"] = "Down"
        ret["CPU Load"] = 0
        ret["Memory Usage"] = (0, 0)
        ret["Disk Usage"] = (0, 0)
    else:
        cpu_index = get_index(cpu_result, "average:")
        mem_index = get_index(cpu_result, "Mem:")
        disk_index = get_index(disk_result, "/")
        mem_used = int(cpu_result[mem_index + 2][:-1]) 
        mem_not_used = int(cpu_result[mem_index][:-1]) - mem_used
        disk_used = float(disk_result[disk_index - 4][:-1])
        disk_not_used = float(disk_result[disk_index - 3][:-1])
        if cpu_index:
            ret["Status"] = "Active"
            ret["CPU Load"] = cpu_result[cpu_index]
            ret["Memory Usage"] = (mem_used / 1024, mem_not_used / 1024) 
            ret["Disk Usage"] = (disk_used, disk_not_used)
    print ret
