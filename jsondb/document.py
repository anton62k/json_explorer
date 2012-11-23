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

    def close(self):
        pass


class Document(Base):

    value_types = [Pattern.INT, Pattern.FLOAT, Pattern.STR]

    def __init__(self, name, **kw):
        type_list = kw.get('pattern').type if kw.get('pattern').type in \
                                                Pattern.list_types else None
        kw.setdefault('type_list', type_list)

        Base.__init__(self, name, class_item=Document, **kw)
        self.parse_kwargs(**kw)

    def add(self, name=None, **kw):
        if not kw.get('pattern'):
            kw.setdefault('pattern', self.get_pattern_item(name))

        return Base.add(self, name=name, **kw)

    def pattern_signal(self, *args, **kw):
        signal_name = kw.get('signal_name')
        if signal_name == 'add':
            field_name = args[0]
            pattern_field = self.pattern.get(field_name)
            self.add(field_name, pattern=pattern_field)

        elif signal_name == 'remove':
            field_name = args[0]
            self.remove(field_name)

        elif signal_name == 'change_type_item':
            self.remove_all()

    def parse_kwargs(self, **kw):
        self.pattern = kw.get('pattern')
        self.pattern.signal.add(self.pattern_signal)
        self.parse_data(kw.get('data', {}))

    def get_pattern_item(self, name=None, **kw):
        return self.pattern.get(name) if not self.type_list else \
                                                        self.pattern.items

    def get_class_item(self, name=None, **kw):
        pattern = self.get_pattern_item(name, **kw)

        if pattern.type in self.value_types:
            return Field

        return self.class_item

    def add_item(self, pattern, sub_data):
        doc = self.add(pattern.name, pattern=pattern,
                         data=sub_data)

        if pattern.type in self.value_types:
            field = doc
            field.set(sub_data or pattern.default)

    def parse_data(self, data):
        if self.type_list:
            pattern = self.pattern.items
            for sub_data in data:
                self.add_item(pattern, sub_data)
        else:
            for pattern in self.pattern:
                sub_data = data.get(pattern.name, {})
                self.add_item(pattern, sub_data)

    def close(self):
        self.pattern.signal.remove(self.pattern_signal)
        Base.close(self)
