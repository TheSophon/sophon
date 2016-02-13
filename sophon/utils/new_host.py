#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import uuid

from sophon.const import SSH_CONFIG_TEMPLATE


def new_host(ip, ssh_secret_key):
    current_home = os.path.expanduser("~")
    key_filename = os.path.join(current_home, ".ssh", str(uuid.uuid1()))
    ssh_config_filename, inventory_filename = (
        os.path.join(current_home, ".ssh", "config"), "./hosts"
    )
    with open(key_filename, "w") as _f:
        _f.write(ssh_secret_key + "\r\n")
    os.chmod(key_filename, 0o600)
    with open(ssh_config_filename, "a+") as _f:
        new_ssh_config = SSH_CONFIG_TEMPLATE.format(
            ip=ip, key_filename=key_filename
        )
        _f.write(new_ssh_config)
    with open(inventory_filename, "a+") as _f:
        _f.write(ip + "\r\n")
