#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import json

from tornado.web import authenticated

from sophon.database import session
from sophon.handlers import BaseHandler
from sophon.models import DeployMeta, UserMeta
from sophon.utils.time_convertor import created2str
from sophon.utils.deploy import do_deploy


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
        session.close()

        do_deploy(deploy_id=deploy_item.id,
                  entry_point=entry_point, user="root",
                  hosts=hosts, repo_uri=repo_uri)

        self.write({
            deploy_item.id: {
                "Taskname": deploy_item.taskname,
                "Status": deploy_item.status,
                "Created": created2str(created=deploy_item.created)
            }
        })


class DeployDetailHandler(BaseHandler):

    @authenticated
    def get(self, deploy_id):
        result = DeployMeta.get_deploy_item_by_id(deploy_id=int(deploy_id))
        result.update({
            "Created": created2str(created=result["Created"])
        })
        self.write(result)
