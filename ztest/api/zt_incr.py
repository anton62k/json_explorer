# coding: utf8
from ztest.test_case import BaseCase
from jsondb.project import Project
from jsondb.pattern import Pattern


class Test(BaseCase):

    def setUp(self):
        self.project = Project()
        self.table = self.project.add('test')

    def test_one_field(self):
        self.table.pattern.add('id', type=Pattern.INT, incr='test.id',
                                                                default=12)

        self.eq(self.table.add(1).get('id').get(), 1)
        self.eq(self.table.get(1).get('id').set(12), 1)
        self.eq(self.table.get(1).get('id').get(), 1)

        self.eq(self.table.add(2).get('id').get(), 2)
        self.eq(self.table.get(2).get('id').set(14), 2)
        self.eq(self.table.get(2).get('id').get(), 2)

        self.eq(self.table.add(3).get('id').get(), 3)
        self.eq(self.table.get(2).get('id').set(14), 2)
        self.eq(self.table.get(2).get('id').get(), 2)

    def test_many_fields(self):
        pass

    def test_many_docs(self):
        pass

    def test_many_tables(self):
        pass


