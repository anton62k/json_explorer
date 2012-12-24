# coding: utf8
from ztest.test_case import BaseCase
from jsondb.project import Project
from jsondb.pattern import Pattern


class Test(BaseCase):

    def setUp(self):
        self.project = Project()
        self.manager = self.project.manager

    def test_add_common(self):
        price = self.manager.add('price', type=Pattern.DICT)
        price.add('type', type=Pattern.STR, values=['coins', 'coins_gold'],
                                                            default='coins')
        price.add('value', type=Pattern.INT, default=10)

        map_object = self.project.add('map_object', type=Pattern.DICT)
        map_object_price = map_object.pattern.add('price', common='price')
        self.eq(price, map_object_price)

        artifact = self.project.add('artifact', type=Pattern.DICT)
        artifact_price = artifact.pattern.add('artifact_price', common='price')
        self.eq(price, artifact_price)

        self.eq(artifact.pattern.add('test', common='unreal_common'), None)

        surprise = self.project.add('surprise', type=Pattern.DICT)
        surprise_price = surprise.pattern.add('list', type=Pattern.LIST,
                                                    item_common='price').items
        self.eq(surprise_price, price)

    def test_change_item_type(self):
        price = self.manager.add('price', type=Pattern.DICT)
        price.add('type', type=Pattern.STR, values=['coins', 'coins_gold'],
                                                            default='coins')
        price.add('value', type=Pattern.INT, default=10)

        map_object = self.project.add('map_object', type=Pattern.DICT)
        map_object_price = map_object.pattern.add('price', type=Pattern.LIST)
        self.neq(map_object_price.items, price)
        map_object_price.change_type_item(None, item_common='price')

        self.eq(price, map_object_price.items)

    def test_document(self):
        pass
