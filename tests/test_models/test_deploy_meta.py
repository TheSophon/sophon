#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from unittest import TestCase

import mock

from sophon.models import DeployMeta
from tests.test_models.conftest import mysql_fixture


class TestDeployMeta(TestCase):

    @mysql_fixture
    def test_insert(self, session):
        _insert_data = DeployMeta(
            taskname="sample_task",
            repo_uri="git@github.com:user/repo.git",
            hosts=[1, 2]
        )
        session.add(_insert_data)

        _query_data = session.query(DeployMeta).first()
        self.assertEqual(_query_data.taskname, "sample_task")
        self.assertEqual(_query_data.status, 0)
        self.assertEqual(_query_data.repo_uri,
                         "git@github.com:user/repo.git")
        self.assertEqual(_query_data.hosts, [1, 2])
        self.assertEqual(_query_data.msg, u"")

    @mysql_fixture
    @mock.patch("sophon.models.deploy_meta.session")
    def test_update_deploy_meta(self, session, _session):
        _commit = mock.Mock()
        _session.commit = _commit
        _insert_data = DeployMeta(
            taskname="sample_task",
            repo_uri="git@github.com:user/repo.git",
            hosts=[1, 2]
        )
        session.add(_insert_data)

        with mock.patch.object(
            DeployMeta, "query", session.query_property()
        ) as _query:
            _id = session.query(DeployMeta).first().id
            DeployMeta.update_deploy_meta(deploy_id=_id,
                                          status=1,
                                          msg=u"placeholder")
            _query_data = session.query(DeployMeta).filter_by(
                id=_id
            ).first()
            self.assertEqual(_query_data.status, 1)
            self.assertEqual(_query_data.msg, u"placeholder")
            _commit.called_once_with()

    @mysql_fixture
    @mock.patch("sophon.models.deploy_meta.session")
    def test_get_all_deploy_summary(self, session, _session):
        _insert_data = DeployMeta(
            taskname="sample_task",
            repo_uri="git@github.com:user/repo.git",
            hosts=[1, 2]
        )
        session.add(_insert_data)

        with mock.patch.object(
            DeployMeta, "query", session.query_property()
        ) as _query:
            summary = DeployMeta.get_all_deploy_summary()
            _id = summary.keys()[0]
            self.assertEqual(summary[_id]["Taskname"], "sample_task")
            self.assertEqual(summary[_id]["Status"], 0)
