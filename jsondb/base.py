# coding: utf8
from jsondb.signal import signal, Signal


class Base(object):

    def __init__(self, name, class_item=None, **kw):
        self.name = str(name)
        self.fields = {}
        self.signal = Signal()
        self.class_item = class_item

    def get_class_item(self, name, **kw):
        if self.class_item:
            return self.class_item

        if kw.get('list', False):
            return BaseList
        return Base

    def set(self, name, **kw):
        return self.fields.setdefault(str(name),
                                self.get_class_item(name, **kw)(name, **kw))

    @signal
    def add(self, name, **kw):
        if not self.get(name):
            return self.set(name, **kw)

    def get(self, name):
        return self.fields.get(str(name))

    @signal
    def remove(self, name):
        item = self.get(name)
        if not item:
            return
        item.close()
        return self.fields.pop(str(name), None)

    @signal
    def remove_all(self):
        for item in self:
            item.close()
        self.fields.clear()
        return True

    def keys(self):
        return sorted(self.fields.keys())

    def data(self):
        data = {}
        for key in self.fields:
            data.setdefault(key, self.fields.get(key).data())
        return data

    def close(self):
        self.remove_all()

    def __getitem__(self, key):
        if isinstance(key, int):
            key = self.keys()[key]
        return self.get(key)

    def length(self):
        return len(self.keys())


class BaseList(Base):

    def data(self):
        data = []
        for item in self:
            data.append(item.data())
        return data

    def add(self, *args, **kw):
        name = str(self.length())
        return self.set(name, **kw)

    def remove(self, index):
        index = int(index)
        rt = Base.remove(self, index)

        if not rt:
            return

        for key in self.keys():
            current_index = int(key)
            new_key = str(current_index - 1)

            if current_index > index:
                item = self.fields.pop(key)
                item.name = new_key
                self.fields.setdefault(new_key, item)

        return rt
