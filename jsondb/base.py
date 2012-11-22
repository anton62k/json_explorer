# coding: utf8
from jsondb.signal import signal, Signal


class Base(object):

    def __init__(self, name, class_item=None, is_list=False, ** kw):
        self.name = str(name)
        self.is_list = is_list
        self.fields = {}
        self.signal = Signal()
        self.class_item = class_item or Base

    def get_class_item(self, name, **kw):
        return self.class_item

    def set(self, name, **kw):
        return self.fields.setdefault(str(name),
                                self.get_class_item(name, **kw)(name, **kw))

    @signal
    def add(self, name=None, **kw):
        if self.is_list:
            name = str(self.length())
        elif self.get(name):
            return
        return self.set(name, **kw)

    def get(self, name):
        return self.fields.get(str(name))

    def remove_in_list(self, index):
        for key in self.keys():
            current_index = int(key)
            new_key = str(current_index - 1)

            if current_index > index:
                item = self.fields.pop(key)
                item.name = new_key
                self.fields.setdefault(new_key, item)

    @signal
    def remove(self, name):
        item = self.get(name)
        if not item:
            return
        item.close()
        rt = self.fields.pop(str(name), None)
        if self.is_list:
            self.remove_in_list(int(name))
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
        data = [] if self.is_list else {}

        for item in self:
            if self.is_list:
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
