# coding: utf8
from ztest.test_case import BaseCase
from jsondb.pattern import Pattern
from jsondb.project import Project


class Test(BaseCase):

    def setUp(self):
        self.project = Project()
        self.table = self.project.add('test', type=Pattern.DYNAMIC_DICT)

    def test_dynamic_dict(self):
        self.eq(self.table.pattern.type, Pattern.DYNAMIC_DICT)
        self.table.pattern.items.add('test', type=Pattern.INT, default=1)

        doc = self.table.add(1)
        self.eq(doc.pattern.type, Pattern.DYNAMIC_DICT)

        item = doc.add(1)
        self.eq(item.name, '1')
        self.eq(item.data(), {'test': 1})

        item = doc.add('test', data={'test': 2})
        self.eq(item.name, 'test')
        self.eq(item.data(), {'test': 2})

        item = doc.add(10, data={'test1': 2})
        self.eq(item.name, '10')
        self.eq(item.data(), {'test': 1})

        self.eq(doc.data(), {'1': {'test': 1}, 'test': {'test': 2},
                             '10': {'test': 1}})

        doc.remove(1)
        self.eq(doc.data(), {'test': {'test': 2}, '10': {'test': 1}})

        doc.remove('test')
        self.eq(doc.data(), {'10': {'test': 1}})

        doc.remove('10')
        self.eq(doc.data(), {})
