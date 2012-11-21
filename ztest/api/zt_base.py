# coding: utf8
from ztest.test_case import BaseCase
from jsondb.base import Base


class Test(BaseCase):

    def setUp(self):
        self.base = Base('')

    def test_get_item(self):
        item = self.base.add('1')

        self.eq(self.base.get(1), item)
        self.eq(self.base.get('1'), item)
        self.eq(self.base['1'], item)
        self.eq(self.base[0], item)

        self.base.remove_all()

        item = self.base.add(1)
        self.eq(self.base.get(1), item)
        self.eq(self.base.get('1'), item)
        self.eq(self.base['1'], item)
        self.eq(self.base[0], item)

        for doc in self.base:
            self.eq(doc, item)

    def test_remove_item(self):
        self.base.add('1')
        self.base.remove('1')

        self.eq(self.base.get('1'), None)
        self.eq(self.base.get(1), None)
        self.eq(self.base['1'], None)

        self.base.add('1')
        self.base.remove(1)

        self.eq(self.base.get('1'), None)
        self.eq(self.base.get(1), None)
        self.eq(self.base['1'], None)
