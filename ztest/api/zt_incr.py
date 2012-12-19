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
        self.table.pattern.add('id', type=Pattern.INT, incr='test.id',
                                                                default=12)
        self.table.pattern.add('value', type=Pattern.INT, incr='test.id',
                                                                default=14)
        self.table.pattern.add('id1', type=Pattern.INT, incr='test.id1',
                                                                default=12)
        self.table.pattern.add('value1', type=Pattern.INT, incr='test.value1',
                                                                default=14)
        self.table.pattern.add('list', type=Pattern.LIST)
        self.table.pattern.get('list').change_type_item(Pattern.INT,
                                                        incr='test.id')

        self.eq(self.table.add(1).get('id').get(), 1)
        self.eq(self.table.get(1).get('value').get(), 2)
        self.eq(self.table.get(1).get('id1').get(), 1)
        self.eq(self.table.get(1).get('value1').get(), 1)

        self.eq(self.table.add(2).get('id').get(), 3)
        self.eq(self.table.get(2).get('value').get(), 4)
        self.eq(self.table.get(2).get('id1').get(), 2)
        self.eq(self.table.get(2).get('value1').get(), 2)

        self.eq(self.table.add(3).get('id').get(), 5)
        self.eq(self.table.get(3).get('value').get(), 6)
        self.eq(self.table.get(3).get('id1').get(), 3)
        self.eq(self.table.get(3).get('value1').get(), 3)

        self.eq(self.table.get(3).get('list').add().get(), 7)
        self.eq(self.table.get(3).get('list').get(0).set(11), 7)
        self.eq(self.table.get(1).get('list').add().get(), 8)
        self.eq(self.table.get(2).get('list').add().get(), 9)
        self.eq(self.table.get(3).get('list').add().get(), 10)
        self.eq(self.table.get(3).get('list').get(1).set(12), 10)

    def test_many_tables(self):
        self.table.pattern.add('id', type=Pattern.INT, incr='global_id',
                                                                default=12)
        self.table2 = self.project.add('test2')
        self.table2.pattern.add('id2', type=Pattern.INT, incr='global_id',
                                                                default=12)
        self.eq(self.table.add(1).get('id').get(), 1)
        self.eq(self.table2.add(10).get('id2').get(), 2)
        self.eq(self.table2.add(2).get('id2').get(), 3)
        self.eq(self.table.add(2).get('id').get(), 4)

