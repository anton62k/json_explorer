# coding: utf8
from ztest.test_case import BaseCase
from jsondb.project import Project
from jsondb.pattern import Pattern


class Test(BaseCase):

    def setUp(self):
        self.project = Project()

        self.artifact = self.project.add('artifact')
        self.artifact.pattern.add('int', type=Pattern.INT)
        self.artifact.pattern.add('str', type=Pattern.STR)
        self.artifact.pattern.add('float', type=Pattern.FLOAT)

        self.table_list = self.project.add('table_list', type=Pattern.LIST)
        self.table_list.pattern.items.add('int', type=Pattern.INT)

        self.table_dynamic = self.project.add('table_dynamic', type=Pattern.DYNAMIC_DICT)
        self.table_dynamic.pattern.items.add('str', type=Pattern.STR)

        self.table_list2 = self.project.add('table_list2', type=Pattern.LIST,
                                            item_type=Pattern.INT)

    def test(self):
        for i in xrange(1, 11):
            doc = self.artifact.add(i)
            self.eq(dict(doc.stats()), {'int': 1, 'float': 1, 'str': 1, 'dict': 1 })

        self.eq(dict(self.artifact.stats()),
                        {'int': 10, 'float': 10, 'document': 10, 'str': 10, 'dict': 10})
        self.eq(dict(self.project.stats()),
            {'int': 10, 'float': 10, 'document': 10, 'str': 10, 'table': 4, 'dict': 10})

        #
        for i in xrange(1, 6):
            doc = self.table_list.add(i)
            self.eq(dict(doc.stats()), {})

            for j in xrange(1, 21):
                item = doc.add()
                self.eq(dict(item.stats()), {'int': 1, 'dict': 1})
                self.eq(dict(doc.stats()), {'int': j, 'dict': j})

        self.eq(dict(self.table_list.stats()),
                        {'int': 100, 'document': 5, 'dict': 100})
        self.eq(dict(self.project.stats()),
            {'int': 110, 'float': 10, 'document': 15, 'str': 10, 'table': 4, 'dict': 110})

        #
        for i in xrange(1, 16):
            doc = self.table_dynamic.add(i)
            self.eq(dict(doc.stats()), {})

            for j in xrange(1, 6):
                item = doc.add(j)
                self.eq(dict(item.stats()), {'str': 1, 'dict': 1})
                self.eq(dict(doc.stats()), {'str': j, 'dict': j})

        self.eq(dict(self.table_dynamic.stats()),
                        {'str': 75, 'document': 15, 'dict': 75})
        self.eq(dict(self.project.stats()),
            {'int': 110, 'float': 10, 'document': 30, 'str': 85, 'table': 4, 'dict': 185})

        #
        for i in xrange(1, 11):
            doc = self.table_list2.add(i)
            self.eq(dict(doc.stats()), {})

            for j in xrange(1, 21):
                item = doc.add()
                self.eq(dict(item.stats()), {'int': 1})
                self.eq(dict(doc.stats()), {'int': j})

        self.eq(dict(self.table_list2.stats()),
                        {'int': 200, 'document': 10})
        self.eq(dict(self.project.stats()),
            {'int': 310, 'float': 10, 'document': 40, 'str': 85, 'table': 4, 'dict': 185})
