# coding: utf8
from jsondb.base import Base
from jsondb.signal import signal
from jsondb.hooks import hook_int_float, hook_str, hook_incr


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
        self.project = kw.get('project')
        data = kw.get('data')

        if data:
            self.parse_data(data)

        else:
            self.parse_kwargs(**kw)

    def get_hook(self):
        if self.type == Pattern.INT and self.incr:
            self.default = 0
            return hook_incr
        if self.type in [Pattern.INT, Pattern.FLOAT]:
            return hook_int_float
        elif self.type in [Pattern.STR]:
            return hook_str

    def parse_kwargs(self, **kw):
        self.type = kw.pop('type', Pattern.DICT)

        for key in ['min', 'max', 'default', 'text', 'values', 'option',
                    'items', 'incr']:
            setattr(self, key, kw.pop(key, None))

        self.hook_set = self.get_hook()

        if self.type in self.default_mapper and not self.default:
            self.default = self.default_mapper.get(self.type)

        if self.type in Pattern.list_types:
            self.create_items(kw.pop('item_type', Pattern.DICT), **kw)

    def create_items(self, type, **kw):
        item_common = kw.get('item_common', None)
        if item_common:
            item = self.project.manager.get(item_common)
            if not item:
                raise PatternError()
        else:
            kw.setdefault('project', self.project)
            item = Pattern('items', type=type, **kw)
        self.items = item

    def parse_data(self, data):
        properties = data.pop('properties', None)
        items = data.pop('items', None)

        self.remove_all()
        self.parse_kwargs(type=data.pop('type'), **data)

        if self.type in self.list_types:
            self.items.parse_data(items)

        elif self.type in Pattern.DICT:
            for field in properties:
                self.add(field, data=properties.get(field))

    @signal
    def change_type_item(self, value, **kw):
        if not self.type in self.list_types:
            raise PatternError()
        self.create_items(value, **kw)
        return True

    def add_from_manager(self, name, manager_name, **kw):
        item = self.project.manager.get(manager_name)
        if item:
            return self.add_to_fields(name, item)

    def add(self, name, manager_name=None, **kw):
        if self.type == Pattern.DICT:
            if manager_name:
                return self.add_from_manager(name, manager_name, **kw)
            else:
                return Base.add(self, name, project=self.project, **kw)
        else:
            raise PatternError()

    def data(self):
        data = {'properties': Base.data(self)} if self.type == Pattern.DICT \
                                                                        else {}

        for key in ['type', 'min', 'max', 'default', 'text', 'values',
                    'option', 'incr']:
            value = getattr(self, key)
            if value:
                data.setdefault(key, value)

        if self.type in Pattern.list_types:
            data.setdefault('items', self.items.data())

        return data
