#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import subprocess


command = {
    "cpu": "top -b -n 1",
    "disk": "df -h .",
    "docker": "docker ps -a",
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
    process = "ansible {0} -a \"{1}\"".format(ip, command["process"])
    process_result = subprocess.Popen(
        process, shell=True, stdout=subprocess.PIPE
    ).stdout.read().split()
    result = []
    if "COMMAND" in "".join(process_result):
        process_index = process_result.index("COMMAND")
        for x in range(0, 5):
            new_index = process_index + 12 * x
            result.append({
                "PID": int(process_result[new_index + 1]),
                "User": process_result[new_index + 2],
                "CPU Usage": float(process_result[new_index + 9]),
                "Memory Usage": float(process_result[new_index + 10]),
                "Time": process_result[new_index + 11],
                "Command": process_result[new_index + 12]
            })
    return result


def get_host_docker_status(ip):
    process = "ansible {0} -a \"{1}\"".format(ip, command["docker"])
    process_result = subprocess.Popen(
        process, shell=True, stdout=subprocess.PIPE
    ).stdout.read().rstrip("\n").split('\n')
    result = []
    if "IMAGE" in "".join(process_result):
        column_names = [
            "Container ID", "Image", "Command",
            "Created", "Status", "Ports", "Names"
        ]
        range_list = map(
            process_result[1].find, map(str.upper, column_names)
        )
        for line in process_result[2:]:
            if line.strip() == "":
                continue
            cur_ps = dict()
            for index, column_name in enumerate(column_names):
                if index + 1 != len(column_names):
                    beg, end = range_list[index], range_list[index + 1]
                    cur_ps[column_name] = line[beg:end].strip()
                else:
                    beg = range_list[index]
                    cur_ps[column_name] = line[beg:].strip()
            result.append(cur_ps)
    return result
