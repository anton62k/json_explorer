# coding: utf8
from ztest.test_case import BaseCase
from jsondb.project import Project


class Test(BaseCase):

    def setUp(self):
        self.project = Project()
        self.table = self.project.add('test')

    def test_project(self):
        self.eq(self.project.values.get('test'), 0)

        self.eq(self.project.values.incr('test'), 1)
        self.eq(self.project.values.get('test'), 1)

        self.eq(self.project.values.incr('test'), 2)
        self.eq(self.project.values.incr('test'), 3)
        self.eq(self.project.values.incr('test'), 4)
        self.eq(self.project.values.get('test'), 4)

        self.eq(self.project.values.get('test1'), 0)
        self.eq(self.project.values.get('test2'), 0)
        self.eq(self.project.values.incr('test2'), 1)
        self.eq(self.project.values.incr('test2'), 2)

