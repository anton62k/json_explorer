# coding: utf8
from ztest.test_case import BaseCase
from jsondb.project import Project
from jsondb.pattern import Pattern
from jsondb.hooks import default_hook_set


class Test(BaseCase):

    def setUp(self):
        self.project = Project()
        self.table = self.project.add('test', type=Pattern.DICT)
        self.table.pattern.add('int', type=Pattern.INT, default=10)
        self.table.pattern.add('float', type=Pattern.FLOAT, default=11.2)
        self.table.pattern.add('str', type=Pattern.STR, default='test')

    def test_default_hook_set(self):
        doc = self.table.add(1, data={'int': 12, 'str': 'test2', 'float': 14.9})
        self.eq(doc.get('int').get(), default_hook_set(None, 10, 12))
        self.eq(doc.get('str').get(), default_hook_set(None, 'test', 'test2'))
        self.eq(doc.get('float').get(), default_hook_set(None, 11.2, 14.9))
