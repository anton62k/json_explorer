# coding: utf8
from jsondb.base import Base
from jsondb.pattern import Pattern


class ManagerPattern(Base):

    def __init__(self, **kw):
        Base.__init__(self, class_item=Pattern)
        self.project = kw.get('project')

    def add(self, name, **kw):
        return Base.add(self, name, project=self.project, **kw)
