# coding: utf8
from jsondb.base import Base
from jsondb.document import Document
from jsondb.pattern import Pattern


class Table(Base):

    def __init__(self, name, pattern=Pattern()):
        Base.__init__(self, name, Document)
        self.pattern = pattern

    def add(self, name, data=None):
        return Base.add(self, name, data=data or {}, pattern=self.pattern)
