# coding: utf8
from jsondb.base import Base
from jsondb.table import Pattern, Table
from collections import Counter


class Values(Counter):

    def get(self, key, default=None):
        return super(Counter, self).get(key, 0)

    def incr(self, key):
        self.update({key: 1})
        return self.get(key)


class Project(Base):

    def __init__(self, name='', **kw):
        self.values = Values()
        Base.__init__(self, name, class_item=Table, **kw)

    def add(self, name, **kw):
        return Base.add(self, name, pattern=Pattern(project=self, **kw))

    def stats(self):
        return Base.stats(self, {'table': self.length()})
