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
        Base.__init__(self, name, class_item=Document, **kw)
        self.parse_kwargs(**kw)

    def pattern_signal(self, *args, **kw):
        if kw.get('signal_name') == 'add':
            field_name = args[0]
            pattern_field = self.pattern.get(field_name)
            self.add(field_name, pattern=pattern_field,
                     is_list=pattern_field.type == Pattern.LIST)

    def parse_kwargs(self, **kw):
        self.pattern = kw.get('pattern')
        self.pattern.signal.add(self.pattern_signal)
        self.parse_data(kw.get('data', {}))

    def get_class_item(self, name=None, **kw):
        pattern = self.pattern.get(name) if not self.is_list else \
                                                        self.pattern.items

        if pattern.type in self.value_types:
            return Field

        return self.class_item

    def parse_data(self, data):

        if self.is_list:
            pattern = self.pattern.items
            for sub_data in data:
                is_list = pattern.type == Pattern.LIST
                doc = self.add(pattern=pattern,
                         data=sub_data, is_list=is_list)

                if pattern.type in self.value_types:
                    field = doc
                    field.set(sub_data or pattern.default)

            return

        for pattern in self.pattern:
            sub_data = data.get(pattern.name, {})
            is_list = pattern.type == Pattern.LIST
            doc = self.add(pattern.name, pattern=pattern,
                             data=sub_data, is_list=is_list)

            if pattern.type in self.value_types:
                field = doc
                field.set(sub_data or pattern.default)

    def close(self):
        self.pattern.signal.remove(self.pattern_signal)
        Base.close(self)
