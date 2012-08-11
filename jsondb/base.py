# coding: utf8
from jsondb.signal import signal, Signal


class Base(object):

    def __init__(self, name, class_item=None, **kw):
        self.name = name
        self.fields = {}
        self.signal = Signal()
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

    @signal
    def add(self, name, **kw):
        name = self.parse_name(name)
        if not self.get(name):
            return self.set(name, **kw)

    def get(self, name):
        return self.fields.get(name)

    @signal
    def remove(self, name):
        item = self.get(name)
        if not item:
            return
        item.close()
        return self.fields.pop(name, None)

    @signal
    def remove_all(self):
        for item in self:
            item.close()
        self.fields.clear()
        return True

    def keys(self):
        return self.fields.keys()

    def data(self):
        data = {}
        for key in self.fields:
            data.setdefault(key, self.fields.get(key).data())
        return data
    
    def close(self):
        self.remove_all()

    def __getitem__(self, key):
        if isinstance(key, int):
            key = sorted(self.fields.keys())[key]
        return self.get(key)
