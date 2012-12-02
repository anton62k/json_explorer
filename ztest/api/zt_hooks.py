# coding: utf8
from ztest.test_case import BaseCase
from jsondb.project import Project
from jsondb.pattern import Pattern
from jsondb.hooks import hook_int_float, hook_str


class Test(BaseCase):

    def setUp(self):
        self.project = Project()
        self.table = self.project.add('test', type=Pattern.DICT)
        self.int_p = self.table.pattern.add('int', type=Pattern.INT, default=10)
        self.float_p = self.table.pattern.add('float', type=Pattern.FLOAT, default=11.2)
        self.str_p = self.table.pattern.add('str', type=Pattern.STR, default='test')

    def test_hook(self):
        doc = self.table.add(1, data={'int': 12, 'str': 'test2', 'float': 14.9})
        self.eq(doc.get('int').get(), hook_int_float(self.int_p, 10, 12))
        self.eq(doc.get('str').get(), hook_str(self.str_p, 'test', 'test2'))
        self.eq(doc.get('float').get(), hook_int_float(self.float_p, 11.2, 14.9))
