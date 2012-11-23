# coding: utf8
from ztest.test_case import BaseCase
from jsondb.pattern import Pattern
from jsondb.project import Project


class Test(BaseCase):

    def setUp(self):
        self.project = Project()
        self.table = self.project.add('test', type=Pattern.DYNAMIC_DICT)

    def test(self):
        self.eq(self.table.pattern.type, Pattern.DYNAMIC_DICT)
        self.table.pattern.items.add('test', type=Pattern.INT, default=1)

        doc = self.table.add(1)
        self.eq(doc.pattern.type, Pattern.DYNAMIC_DICT)

        item = doc.add()
        self.eq(item.name, '0')
        self.eq(item.data(), {'test': 1})

        item = doc.add(data={'test': 2})
        self.eq(item.name, '1')
        self.eq(item.data(), {'test': 2})

        item = doc.add(data={'test1': 2})
        self.eq(item.name, '2')
        self.eq(item.data(), {'test': 1})

        self.eq(doc.data(), {'0': {'test': 1}, '1': {'test': 2}, '2': {'test': 1}})
