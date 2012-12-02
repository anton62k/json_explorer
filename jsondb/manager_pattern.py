# coding: utf8
from jsondb.base import Base
from jsondb.pattern import Pattern


class ManagerPattern(Base):

    def __init__(self):
        Base.__init__(self, class_item=Pattern)
