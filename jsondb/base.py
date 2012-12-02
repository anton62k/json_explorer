# coding: utf8
from jsondb.signal import signal, Signal
from collections import Counter


class Base(object):

    def __init__(self, name='', class_item=None, type_list=None, ** kw):
        self.name = self.parse_name(name)
        self.type_list = type_list
        self.fields = {}
        self.signal = Signal()
        self.class_item = class_item or Base

    def parse_name(self, name):
        return str(name)

    def get_class_item(self, **kw):
        return self.class_item

    def set(self, name, **kw):
        return self.fields.setdefault(self.parse_name(name),
                            self.get_class_item(name=name, **kw)(name, **kw))

    @signal
    def add(self, name=None, **kw):
        if self.type_list == 'list':
            name = str(self.length())
        elif not name or self.get(name):
            return
        return self.set(name, **kw)

    def get(self, name):
        return self.fields.get(self.parse_name(name))

    def update_list(self, removed_index):
        for key in self.keys():
            current_index = int(key)
            new_key = str(current_index - 1)

            if current_index > removed_index:
                item = self.fields.pop(key)
                item.name = new_key
                self.fields.setdefault(new_key, item)

    @signal
    def remove(self, name):
        item = self.get(name)
        if not item:
            return
        item.close()
        rt = self.fields.pop(self.parse_name(name), None)
        if self.type_list == 'list':
            self.update_list(int(name))
        return rt

    @signal
    def remove_all(self):
        for item in self:
            item.close()
        self.fields.clear()
        return True

    def keys(self):
        return sorted(self.fields.keys())

    def data(self):
        data = [] if self.type_list == 'list' else {}

        for item in self:
            if self.type_list == 'list':
                data.append(item.data())
            else:
                data.setdefault(item.name, item.data())
        return data

    def close(self):
        self.remove_all()

    def __getitem__(self, key):
        if isinstance(key, int):
            key = self.keys()[key]
        return self.get(key)

    def length(self):
        return len(self.keys())

    def stats(self, add=None):
        counter = Counter()
        for item in self:
            counter.update(item.stats())
        counter.update(add)
        return counter
