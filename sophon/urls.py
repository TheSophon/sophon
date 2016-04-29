#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from sophon.handlers.index import IndexHandler
from sophon.handlers.user import (
    LoginHandler,
    LogoutHandler,
    GetUserInfoHandler,
    UserRegisterHandler,
    UserPasswordHanlder
)
from sophon.handlers.host import (
    HostHandler, HostStatusHandler,
    HostProcessStatusHandler, HostDockerStatusHandler
)
from sophon.handlers.deploy import DeployHandler, DeployDetailHandler
from sophon.handlers.ssh_permission import SSHPermissionHandler


URL_PATTERNS = [
    (r"/", IndexHandler),
    (r"/api/user/login", LoginHandler),
    (r"/api/user/logout", LogoutHandler),
    (r"/api/user/reg", UserRegisterHandler),
    (r"/api/user/info", GetUserInfoHandler),
    (r"/api/user/password", UserPasswordHanlder),
    (r"/api/host", HostHandler),
    (r"/api/host/status", HostStatusHandler),
    (r"/api/host/(\d+)/process_status", HostProcessStatusHandler),
    (r"/api/host/ssh_permission", SSHPermissionHandler),
    (r"/api/host/dockers_status", HostDockerStatusHandler),
    (r"/api/deploy", DeployHandler),
    (r"/api/deploy/(\d+)", DeployDetailHandler)
]
