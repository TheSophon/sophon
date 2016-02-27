#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import tempfile
import subprocess
from multiprocessing import Process

from sophon.const import (
    DEPLOY_TEMPLATE_PART_VARS, DEPLOY_TEMPLATE_PART_TASK
)
from sophon.models import DeployMeta, HostMeta


def deploy(deploy_id, entry_point, user, hosts_ip, repo_uri):
    deploy_playbook = DEPLOY_TEMPLATE_PART_VARS.format(
        hosts_ip_arg=",".join(hosts_ip),
        user_arg=user,
        app_name_arg=entry_point,
        repo_uri_arg=repo_uri
    ) + DEPLOY_TEMPLATE_PART_TASK
    with tempfile.NamedTemporaryFile(suffix=".yml") as tmp_playbook:
        tmp_playbook.write(deploy_playbook)
        tmp_playbook.flush()
        msg = subprocess.Popen(
            "ansible-playbook " + tmp_playbook.name,
            shell=True,
            stdout=subprocess.PIPE
        ).stdout.read()
        status = 1 if "FAILED=0" in msg.upper() else 2
        DeployMeta.update_deploy_meta(deploy_id=deploy_id,
                                      status=status, msg=msg)



def do_deploy(deploy_id, entry_point, user, hosts, repo_uri):
    hosts_status = HostMeta.get_all_hosts_status()
    hosts_ip = [hosts_status[_id]["IP"] for _id in hosts]

    p = Process(target=deploy,
                kwargs={
                    "deploy_id": deploy_id,
                    "entry_point": entry_point,
                    "user": user,
                    "hosts_ip": hosts_ip,
                    "repo_uri": repo_uri
                })
    p.start()
