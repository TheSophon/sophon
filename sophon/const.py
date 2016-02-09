#!/usr/bin/env python2
# -*- coding: utf-8 -*-

DEPLOY_TEMPLATE_PART_VARS = """
---

- hosts: {hosts_ip_arg}
  user: {user_arg}

  vars:
    app_name: {app_name_arg}
    repo_url: {repo_uri_arg}
    repo_remote: origin
    repo_version: master
    webapps_dir: /app
"""

DEPLOY_TEMPLATE_PART_TASK = """

  tasks:
    - name: clone code from repository
      action: git repo={{repo_url}} dest={{webapps_dir}}/{{app_name}} remote={{repo_remote}} version={{repo_version}}
      
    - name: install dependencies into virtualenv
      action: pip requirements={{webapps_dir}}/{{app_name}}/requirements.txt virtualenv={{webapps_dir}}/{{app_name}}/venv state=present

    - name: add supervisor config
      action: file src={{webapps_dir}}/{{app_name}}/deploy/{{app_name}}.conf dest=/etc/supervisor/conf.d/{{app_name}}.conf state=link
      notify:
        - restart app

    - name: reload supervisor
      action: command supervisorctl reload
    
    - name: start app
      action: supervisorctl name={{app_name}} state=started

  handlers:
    - name: restart app
      action: supervisorctl name={{app_name}} state=restarted
"""
