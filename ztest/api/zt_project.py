# coding: utf8

from jsondb.project import Project
from ztest.test_case import BaseCase
from jsondb.table import Table
from jsondb.pattern import Pattern


class ProjectTest(BaseCase):

    def setUp(self):
        self.project = Project()
        self.table_name = 'artifact'

    def test_add_table(self):
        self.isinstance(self.project, Project)

        table = self.project.add(self.table_name)
        self.isinstance(table, Table)
        self.eq(table.name, self.table_name)
        self.eq(self.project.get(self.table_name), table)

        self.isinstance(table.pattern, Pattern)
        self.eq(table.pattern.type, Pattern.DICT)
        self.eq(table.pattern.fields, {})

    def test_dublicate_add_table(self):
        self.project.add(self.table_name)
        self.eq(self.project.add(self.table_name), None)

    def test_remove_table(self):
        table = self.project.add(self.table_name)

        self.eq(self.project.remove('artifact2'), None)
        self.eq(self.project.get(self.table_name), table)

        self.eq(self.project.remove(self.table_name), table)
        self.eq(self.project.get(self.table_name), None)

    def test_remove_all_table(self):
        table1 = self.project.add('test1')
        table2 = self.project.add('test2')

        self.eq(self.project.get('test1'), table1)
        self.eq(self.project.get('test2'), table2)
        self.eq(self.project.fields, {'test1': table1, 'test2': table2})

        self.eq(self.project.remove_all(), True)

        self.eq(self.project.get('test1'), None)
        self.eq(self.project.get('test2'), None)
        self.eq(self.project.fields, {})

    def test_add_table_with_pattern(self):
        table = self.project.add(self.table_name, type=Pattern.DYNAMIC_DICT)

        self.eq(table.pattern.type, Pattern.DYNAMIC_DICT)

    def test_project_values(self):
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
