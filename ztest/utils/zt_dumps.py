# coding: utf8
from ztest.test_case import BaseCase
from jsondb.utils import dumps
from jsondb.project import Project
from jsondb.pattern import Pattern
import shutil
import os
import codecs
import json
import tempfile


class Test(BaseCase):

    def setUp(self):
        self.project = Project()

        test1 = self.project.add('test1')
        test1.pattern.add('test1', type=Pattern.INT, default=1)
        test2 = self.project.add('test2')
        test2.pattern.add('test2', type=Pattern.INT, default=2)
        test3 = self.project.add('test3')
        test3.pattern.add('test3', type=Pattern.INT, default=3)
        test4 = self.project.add('test4', type=Pattern.LIST)
        test4.pattern.items.add('field4', type=Pattern.STR, default='test4')
        test5 = self.project.add('test5', type=Pattern.DYNAMIC_DICT)
        test5.pattern.items.add('field5', type=Pattern.STR, default='test5')

        test1.add('1', data={'test1': 1})
        test1.add('2', data={'test1': 2})
        test1.add('3', data={'test1': 3})
        test1.add('10', data={'test1': 4})
        test1.add('11', data={'test1': 5})

        test2.add('test1', data={'test2': 6})
        test2.add('test2', data={'test2': 7})
        test2.add('test3', data={'test2': 8})

        test3.add('test_1', data={'test3': 9})
        test3.add('test_2', data={'test3': 10})
        test3.add('test_3', data={'test3': 11})

        test4.add(1, data=[{'field4': 'test4_1'}])
        test4.add(2, data=[{'field4': 'test4_2'}])

        test5.add(1).add('1', data={'field5': 'test5_1'})
        test5.add(2).add('test', data={'field5': 'test5_2'})
        test5.add(3).add('test')

        self.path = tempfile.mkdtemp()

    def clear_project(self):
        shutil.rmtree(self.path)

    def get_data(self, table, doc):
        filepath = os.path.join(self.path, table.name, '%s.json' % doc.name)
        f = codecs.open(filepath, 'r', 'utf8')
        json_str = f.read()
        f.close()
        return json.loads(json_str, 'utf8')

    def test_all_dumps(self):
        dumps(self.path, self.project)

        for table in self.project:
            for doc in table:
                file_data = self.get_data(table, doc)
                self.eq(doc.data(), file_data)

        self.clear_project()

    def test_remove_doc(self):
        dumps(self.path, self.project)

        self.project.get('test2').remove('test1')
        dumps(self.path, self.project)

        filepath = os.path.join(self.path, 'test2', 'test1.json')
        self.eq(os.path.exists(filepath), False)

        self.clear_project()

    def test_remove_table(self):
        dumps(self.path, self.project)

        self.project.remove('test2')
        dumps(self.path, self.project)

        filepath = os.path.join(self.path, 'test2')
        self.eq(os.path.exists(filepath), False)

        self.clear_project()
