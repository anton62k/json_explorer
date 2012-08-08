# coding: utf8


def signal(f):

    def w(obj, *args, **kw):
        rt = f(obj, *args, **kw)
        if rt:
            obj.signal.dispatch(signal_name=f.func_name, *args, **kw)
        return rt

    return w


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
