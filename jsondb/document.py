# coding: utf8
from jsondb.base import Base
from jsondb.pattern import Pattern


class Field(object):

    def __init__(self, name, **kw):
        self.name = name
        self.pattern = kw.get('pattern')
        self.value = self.pattern.default

    def get(self):
        return self.value

    def set(self, value):

        if self.pattern.type in [Pattern.INT, Pattern.FLOAT]:

            if self.pattern.values and not value in self.pattern.values:
                return self.get()

            if not self.pattern.min == None and value < self.pattern.min:
                return self.get()

            if not self.pattern.max == None and value > self.pattern.max:
                return self.get()

        if self.pattern.type == Pattern.STR:

            if self.pattern.values and not value in self.pattern.values:
                return self.get()

        self.value = value

        return self.get()

    def data(self):
        return self.get()


class Document(Base):

    value_types = [Pattern.INT, Pattern.FLOAT, Pattern.STR]

    def __init__(self, name, **kw):
        Base.__init__(self, name, Document)
        self.parse_kwargs(**kw)

    def pattern_signal(self, *args, **kw):
        if kw.get('signal_name') == 'add':
            field_name = args[0]
            pattern_field = self.pattern.get(field_name)
            self.add(field_name, pattern=pattern_field)

    def parse_kwargs(self, **kw):
        self.pattern = kw.get('pattern')
        self.pattern.signal.add(self.pattern_signal)
        self.create(kw.get('data', {}))

    def get_class_item(self, name):
        pattern_item = self.pattern.get(name)

        if pattern_item.type in self.value_types:
            return Field

        return self.class_item

    def create_dict(self, data):
        for sub_pattern in self.pattern:

            sub_data = data.get(sub_pattern.name, None)

            field = self.add(sub_pattern.name, pattern=sub_pattern,
                             data=sub_data)

            if sub_pattern.type in self.value_types:
                field.set(sub_data or sub_pattern.default)

    def create(self, data):
        if self.pattern.type == Pattern.DICT:
            self.create_dict(data)

    def close(self):
        # self.pattern.signal.remove(self.pattern_signal)
        for doc in self:
            doc.close()
