# coding: utf8
from ztest.test_case import BaseCase
from jsondb.utils import dumps
from jsondb.project import Project
from jsondb.pattern import Pattern


class Test(BaseCase):

    def setUp(self):
        self.project = Project()

        test1 = self.project.add('test1')
        test1.pattern.add('test1', type=Pattern.INT, default=1)
        test2 = self.project.add('test2')
        test2.pattern.add('test2', type=Pattern.INT, default=2)
        test3 = self.project.add('test3')
        test3.pattern.add('test3', type=Pattern.INT, default=3)

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

    def test_dumps(self):
        dumps('./', self.project)
