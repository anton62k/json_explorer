# coding: utf8
from ztest.test_case import BaseCase
from jsondb.project import Project
from jsondb.pattern import Pattern


class Test(BaseCase):

    def setUp(self):
        self.project = Project()
        self.manager = self.project.manager

        self.price = self.manager.add('price', type=Pattern.DICT)
        self.price.add('type', type=Pattern.STR, values=['coins', 'coins_gold'],
                                                            default='coins')
        self.price.add('value', type=Pattern.INT, default=10)

    def test_add_common(self):
        map_object = self.project.add('map_object', type=Pattern.DICT)
        map_object_price = map_object.pattern.add('price', common='price')
        self.eq(self.price, map_object_price)

        artifact = self.project.add('artifact', type=Pattern.DICT)
        artifact_price = artifact.pattern.add('artifact_price', common='price')
        self.eq(self.price, artifact_price)

        self.eq(artifact.pattern.add('test', common='unreal_common'), None)

        surprise = self.project.add('surprise', type=Pattern.DICT)
        surprise_price = surprise.pattern.add('list', type=Pattern.LIST,
                                                    item_common='price').items
        self.eq(surprise_price, self.price)

    def test_change_item_type(self):
        map_object = self.project.add('map_object', type=Pattern.DICT)
        map_object_price = map_object.pattern.add('price', type=Pattern.LIST)
        self.neq(map_object_price.items, self.price)
        map_object_price.change_type_item(None, item_common='price')

        self.eq(self.price, map_object_price.items)

    def test_common_root(self):
        artifact = self.project.add('artifact', pattern_name='price')
        self.eq(artifact.pattern, self.price)

    def test_document(self):
        artifact = self.project.add('artifact')
        artifact.pattern.add('price', common='price')
        artifact.pattern.add('test', type=Pattern.STR, default='temp')

        ruin = self.project.add('ruin')
        ruin.pattern.add('price', common='price')
        ruin.pattern.add('value', type=Pattern.INT, default=0)

        #
        art1 = artifact.add(1)
        self.eq(art1.data(),
                {'test': 'temp', 'price': {'type': 'coins', 'value': 10}})
        art1.get('price.value').set(20)
        art1.get('test').set('temp1')
        art1.get('price.type').set('coins_gold')
        self.eq(art1.data(),
            {'test': 'temp1', 'price': {'type': 'coins_gold', 'value': 20}})

        #
        r = ruin.add('mo2')
        self.eq(r.data(),
                {'value': 0, 'price': {'type': 'coins', 'value': 10}})
        r.get('price.value').set(22)
        r.get('value').set(2)
        r.get('price.type').set('coins_gold')
        self.eq(r.data(),
            {'value': 2, 'price': {'type': 'coins_gold', 'value': 22}})

        # change common pattern
        self.price.add('chance', type=Pattern.LIST, item_type=Pattern.INT)

        art1.get('price.chance').add().set(1)
        art1.get('price.chance').add().set(2)
        art1.get('price.chance').add()
        self.eq(art1.data(), {'test': 'temp1', 'price': {'type': 'coins_gold',
                            'value': 20, 'chance': [1, 2, 0]}})

        r.get('price.chance').add().set(111)
        r.get('price.chance').add().set(26)
        self.eq(r.data(), {'value': 2, 'price': {'type': 'coins_gold',
                            'value': 22, 'chance': [111, 26]}})
