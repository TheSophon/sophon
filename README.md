Sophon
======

[![Build Status](https://travis-ci.org/TheSophon/sophon.svg?branch=master)](https://travis-ci.org/TheSophon/sophon)
[![Coverage Status](https://coveralls.io/repos/TheSophon/sophon/badge.svg?branch=master)](https://coveralls.io/r/TheSophon/sophon?branch=master)

Simple IT automation web service based on Ansible.

This back-end project only provide RESTFul API. If you want to find a front-end project for this web service, you should visit [ansible-webapp](https://github.com/TheSophon/sophon-webapp).

Support system
---

Ubuntu 14.04 / Debian Jessie

Requirements
---

Python 2.7

MySQL

Installation
---

You could use the project [ansible-role-sophon](https://github.com/TheSophon/ansible-role-sophon) to deploy the whole project with front-end project automatically.

Or you could install stand-alone Sophon by following steps:

1. Use `virtualenv` to generate a virutal Python environment, such as `virtualenv venv`.

2. Clone the whole project, and use `python setup.py install` to install whole project and its dependencies.

3. There is two entry points for Sophon, one is `sophon`, which is used for starting web service, the other is `sophon-cron`, which is used for getting data from all hosts. You may use `supervisor` to control them.

API
---

`/api/user/login`: related to login.

* Method POST: used for login.

  * Argument: username(string), password(string)
  
  * return `id`, `username`, `type` of current user in json if succeed, else return an error message.

`/api/user/logout`: related logout.

* Method GET: used for logout.

  * Argument: None

  * return nothing.

`/api/user/reg`:  related to registering new users.

* Method POST, note that the type of current use must be 1(ops): used for registering new users.

  * Argument: username(string), password(string), type(int), public\_key(string)

  * return `{ msg: "sucess" }` if succeed, else return an error message.

`/api/user/info`: related to the information of current user.

* Method GET: used for getting the information of current user.

  * Argument: None

  * return `id`, `username`, `type` of current user in json if succeed, else return nothing.

`/api/user/password`: related to the password of current user.

* Method PUT: used for changing the password of current user.

  * Argument: password(string)

  * return `{ msg: "sucess" }` if succeed, else return an error message.

`/api/host`: related to hosts.

* Method POST: used for adding a new host.

  * Argument: hostname(string), ip(string), ssh\_secret\_key(string)

  * return the status of new host if succeed, else return an error message.

`/api/host/status`: related to the status of hosts.

* Method GET: get the status of all hosts.

  * Argument: None

  * return the status of all hosts, include hostname, IP address, status, CPU load, memory usage and disk usage.

`/api/host/(\d+)/process_status`: related to the status of processes on hosts.

* Method GET: get the status of processes on specific host.

  * Argument: None

  * return the status of all processes on specific host, include IP, user, CPU usage, memory usage, time and command if succeed, else return an error message.

`/api/host/ssh_permission`: related to the permission of SSH for current user.

* Method GET: get the permission of SSH of all hosts for current user.

  * Argument: None

  * return the permission of SSH of all hosts for current user if succeed, else return an error message.

* Method PATCH: change the permission of SSH of specific hosts for current user (only support to get the permission now).

  * Argument: host id(int)

  * return the status of new host if succeed, else return an error message.

`/api/host/dockers_status`: related to the status of containers on all hosts.

* Method GET: get the status of containers on all hosts.

  * Argument: None

  * return the status of all containers on all hosts, include container ID, image, command, created time, status, ports and name if succeed, else return an error message.

`/api/deploy`: related to the deploy tasks.

* Method GET: get the status of all deploy tasks.

  * Argument: None

  * return the status of all deploy tasks, include task name, status and created time if succeed, else return an error message.

* Method POST: create a new deploy task.

  * Argument: taskname(string), repo\_uri(string), entry\_point(string), host(string)

  * return the status of new deploy task if succeed, else return an error message.

`/api/deploy/(\d+)`: related to the deploy task.

* Method GET: get the status of specific deploy task.

  * Argument: None

  * return the status of specific deploy task, include task name, status, created time, repo URI, entry point, host and message, else return an error message.

License
---

MIT
