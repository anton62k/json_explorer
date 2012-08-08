# coding: utf8
from jsondb.base import Base
from jsondb.table import Pattern, Table


class Project(Base):

    def __init__(self, name=''):
        Base.__init__(self, name, Table)

    def add(self, name, pattern=None):
        return Base.add(self, name, pattern=pattern or Pattern())
