#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import uuid


def new_user_public_key(ssh_public_key):
    current_home = os.path.expanduser("~")
    pub_key_filename = os.path.join(
        current_home, ".ssh", str(uuid.uuid1()) + ".pub"
    )
    with open(pub_key_filename, "w") as _f:
        _f.write(ssh_public_key + "\r\n")
    return pub_key_filename
