# coding: utf8
from jsondb.base import Base
from jsondb.table import Pattern, Table
from jsondb.manager_pattern import ManagerPattern


class Project(Base):

    def __init__(self, name='', **kw):
        self.manager = ManagerPattern()
        Base.__init__(self, name, class_item=Table, **kw)

    def add(self, name, **kw):
        return Base.add(self, name, pattern=Pattern(**kw))

    def stats(self):
        return Base.stats(self, {'table': self.length()})
