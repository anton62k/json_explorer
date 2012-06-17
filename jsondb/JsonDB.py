#coding: utf8

import os
import json
import codecs


class Loader(object):

    def __init__(self, path):
        self.path = path

    @property
    def balance_path(self):
        return os.path.join(self.path, 'balance')

    def collection_path(self, collection):
        return os.path.join(self.balance_path, collection)

    def doc_path(self, collection, doc):
        return os.path.join(self.collection_path(collection), doc)

    def collections(self):
        return os.listdir(self.balance_path)

    def docs(self, collection):
        return os.listdir(self.collection_path(collection))

    def get_doc(self, collection, doc):
        return json.loads(codecs.open(self.doc_path(collection, doc), 'r', 'utf-8').read())


class Collection(object):

    def __init__(self, name):
        self.name = name
        self.doc = {}

    def add(self, name, data):
        doc[name] = Document(data)
        pass


class Document(object):

    def __init__(self, name):
        self.name = name


class JsonDB(object):

    def __init__(self, local_path):
        self.local_path = local_path
        self.collection = {}

    def add_collection(self, name):
        collection = Collection(name)
        self.collection[name] = collection
        return collection

    def load(self):
        loader = Loader(self.local_path)

        for collection_name in loader.collections():
            collection = self.add_collection(collection_name)

            for doc_name in loader.docs(collection_name):
                doc = loader.get_doc(collection_name, doc_name)
                collection.add(doc)
