# coding: utf8


class Cursor(object):

    def __init__(self, prefix=''):
        self.prefix = prefix

    def clone(self, add_prefix):
        if (self.prefix):
            add_prefix = '%s.%s' % (self.prefix, add_prefix)
        return Cursor(add_prefix)


class Document(object):

    def parse(self, k, v):
        if isinstance(v, dict):
            v = Document(v, self.__cursor.clone(k))
        setattr(self, k, v)

    def __init__(self, data, cursor=Cursor()):
        self.__cursor = cursor
        for k, v in data.iteritems():
            self.parse(k, v)

    def __getitem__(self, key):
        return getattr(self, key)

    def get_prefix(self):
        return self.__cursor.prefix
