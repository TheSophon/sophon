#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import json

from tornado.web import authenticated

from sophon.database import session
from sophon.handlers import BaseHandler
from sophon.models import DeployMeta, UserMeta
from sophon.utils.time_convertor import created2str


class DeployHandler(BaseHandler):

    @authenticated
    def get(self):
        result = DeployMeta.get_all_deploy_summary()
        for key in result.keys():
            result[key]["Created"] = created2str(
                result[key]["Created"]
            )
        self.write(result)

    @authenticated
    def post(self):
        taskname = self.get_argument("taskname")
        repo_uri = self.get_argument("repo_uri")
        entry_point = self.get_argument("entry_point")
        hosts = json.loads(self.get_argument("hosts"))

        username = self.get_secure_cookie("username")
        user_id = UserMeta.query.filter_by(username=username).first().id

        deploy_item = DeployMeta(taskname=taskname, user_id=user_id,
                                 repo_uri=repo_uri, entry_point=entry_point,
                                 hosts=hosts)
        session.add(deploy_item)
        session.commit()

        self.write({
            deploy_item.id: {
                "Taskname": deploy_item.taskname,
                "Status": deploy_item.status,
                "Created": created2str(deploy_item.created)
            }
        })
