# coding: utf8


class Signal():

    def __init__(self):
        self.listeners = []

    def add(self, listener):
        self.listeners.append(listener)

    def remove(self, listener):
        self.listeners.remove(listener)

    def dispatch(self, *args, **kw):
        for listener in self.listeners:
            listener(*args, **kw)


class Base(object):

    def __init__(self, name, class_item=None, **kw):
        self.name = name
        self.fields = {}
        self.class_item = class_item or Base

    def get_class_item(self, name):
        return self.class_item

    def set(self, name, **kw):
        return self.fields.setdefault(name,
                                      self.get_class_item(name)(name, **kw))

    def parse_name(self, name):
        if type(name) is str and name.isdigit():
            name = int(name)
        return name

    def add(self, name, **kw):
        name = self.parse_name(name)
        return self.get(name) or self.set(name, **kw)

    def get(self, name):
        return self.fields.get(name)

    def remove(self, name):
        return self.fields.pop(name, None)

    def remove_all(self):
        self.fields = {}

    def keys(self):
        return self.fields.keys()

    def data(self):
        data = {}
        for key in self.fields:
            data.setdefault(key, self.fields.get(key).data())
        return data

    def __getitem__(self, key):
        if isinstance(key, int):
            key = sorted(self.fields.keys())[key]
        return self.get(key)


class Project(Base):

    def __init__(self, name=''):
        Base.__init__(self, name, Table)

    def add(self, name, pattern=None):
        return Base.add(self, name, pattern=pattern or Pattern())


class Pattern(Base):

    DICT = 'dict'
    LIST = 'list'
    DYNAMIC_DICT = 'dynamic_dict'
    INT = 'int'
    FLOAT = 'float'
    STR = 'str'

    default_mapper = {
        INT: 0,
        FLOAT: 0,
        STR: ''
    }

    list_types = [LIST, DYNAMIC_DICT]

    def __init__(self, name='', **kw):
        Base.__init__(self, name, Pattern)
        self.signal = Signal()
        data = kw.get('data')

        if data:
            self.parse_data(data)

        else:
            self.parse_kwargs(**kw)

    def parse_kwargs(self, **kw):
        self.type = kw.get('type', Pattern.DICT)

        for key in ['min', 'max', 'default', 'text', 'values', 'option',
                    'items']:
            setattr(self, key, kw.get(key, None))

        if self.type in self.default_mapper and not self.default:
            self.default = self.default_mapper.get(self.type)

        if self.type in Pattern.list_types:
            self.items = Pattern('$items')

    def parse_data(self, data):
        f = data.pop('$format')
        self.change_type(f.pop('type'), **f)

        if self.type in self.list_types:
            self.items.parse_data(data.pop('$items'))

        elif self.type in Pattern.DICT:
            for field in data:
                self.add(field, data=data.get(field))

    def change_type(self, value, **kw):
        self.remove_all()
        self.parse_kwargs(type=value, **kw)
        self.signal.dispatch(signal='change', type=value)

    def get(self, name):
        if self.type == Pattern.DICT:
            return Base.get(self, name)

    def add(self, name, pattern=None, **kw):
        if self.type == Pattern.DICT:
            p = Base.add(self, name, pattern=pattern or Pattern(), **kw)
            self.signal.dispatch(signal='add', name=name)
            return p

    def remove(self, name):
        p = Base.remove(self, name)
        self.signal.dispatch(signal='remove', name=name)
        return p

    def data(self):
        data = Base.data(self)
        f = data.setdefault('$format', {})

        for key in ['type', 'min', 'max', 'default', 'text', 'values',
                    'option']:
            value = getattr(self, key)
            if value:
                f.setdefault(key, value)

        if self.type in Pattern.list_types:
            data.setdefault('$items', self.items.data())

        return data


class Table(Base):

    def __init__(self, name, pattern=Pattern()):
        Base.__init__(self, name, Document)
        self.pattern = pattern

    def add(self, name, data=None):
        return Base.add(self, name, data=data or {}, pattern=self.pattern)

    def update(self):
        '''
        Bad method
        '''
        for doc in self:
            self.fields[doc.name] = Document(doc.name, pattern=self.pattern,
                                             data=doc.data())


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
        print args, kw

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
