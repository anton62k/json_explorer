# coding: utf8
from jsondb.base import Base
from jsondb.signal import signal


class PatternError(Exception):

    def __init__(self):
        Exception.__init__(self, 'error method, this pattern is bad type')


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
        Base.__init__(self, name, class_item=Pattern, **kw)
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
            self.items = Pattern('$items',
                                 type=kw.get('item_type', Pattern.DICT))

    def parse_data(self, data):
        f = data.pop('$format')
        self.change_type(f.pop('type'), **f)

        if self.type in self.list_types:
            self.items.parse_data(data.pop('$items'))

        elif self.type in Pattern.DICT:
            for field in data:
                self.add(field, data=data.get(field))

    @signal
    def change_type_item(self, value, **kw):
        if not self.type in self.list_types:
            raise PatternError()
        self.items = Pattern('$items', type=value, **kw)
        return True

    def add(self, name, **kw):
        if self.type == Pattern.DICT:
            return Base.add(self, name, **kw)
        else:
            raise PatternError()

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
