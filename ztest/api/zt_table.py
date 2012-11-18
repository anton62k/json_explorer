# coding: utf8
from ztest.test_case import BaseCase
from jsondb.project import Project
from jsondb.document import Document


class TableTest(BaseCase):

    def setUp(self):
        self.project = Project()
        self.table = self.project.add('test')

    def test_add(self):
        self.eq(self.table.name, 'test')

        doc = self.table.add('1')
        self.isinstance(doc, Document)
        self.eq(doc.name, 1)

        doc2 = self.table.add('test')
        self.isinstance(doc2, Document)
        self.eq(doc2.name, 'test')

    def test_add_dublicate(self):
        self.neq(self.table.add('1'), None)
        self.eq(len(self.table.keys()), 1)

        self.eq(self.table.add('1'), None)
        self.eq(len(self.table.keys()), 1)

        self.eq(self.table.add(1), None)
        self.eq(len(self.table.keys()), 1)

        self.neq(self.table.add(2), None)
        self.eq(len(self.table.keys()), 2)

        self.neq(self.table.add('test'), None)
        self.eq(len(self.table.keys()), 2)

