# coding: utf8
from ztest.test_case import BaseCase
from jsondb.pattern import Pattern
from jsondb.project import Project
from jsondb.document import Field, Document


class Test(BaseCase):

    def setUp(self):
        self.project = Project()
        self.table = self.project.add('test')
        self.pattern = self.table.pattern

    def test_add_int_pattern(self):
        doc = self.table.add(1)
        self.eq(doc.pattern.type, Pattern.DICT)

        pattern_field_int = self.pattern.add('field_int', type=Pattern.INT, default=12)
        self.isinstance(doc.get('field_int'), Field)
        self.eq(doc.get('field_int').pattern.type, Pattern.INT)
        self.eq(doc.get('field_int').pattern, pattern_field_int)
        self.eq(doc.get('field_int').get(), pattern_field_int.default)

    def test_add_list_pattern(self):
        doc = self.table.add(1)

        pattern_list = self.pattern.add('field_list', type=Pattern.LIST)
        self.isinstance(doc.get('field_list'), Document)
        self.eq(doc.get('field_list').pattern.type, Pattern.LIST)
        self.eq(doc.get('field_list').pattern, pattern_list)
