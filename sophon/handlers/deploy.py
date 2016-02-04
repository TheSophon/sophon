#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from tornado.web import authenticated

from sophon.handlers import BaseHandler
from sophon.models import DeployMeta
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
        pass
