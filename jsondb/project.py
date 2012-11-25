# coding: utf8
from jsondb.base import Base
from jsondb.table import Pattern, Table


class Project(Base):

    root_table_types = [Pattern.DYNAMIC_DICT, Pattern.DICT]

    def __init__(self, name='', **kw):
        Base.__init__(self, name, class_item=Table, **kw)

    def add(self, name, **kw):
        return Base.add(self, name, pattern=Pattern(**kw))
