# coding: utf8
from ztest.test_case import BaseCase
from jsondb.base import Base, BaseList


class Test(BaseCase):

    def setUp(self):
        self.base = Base('')

    def test_get_item(self):
        item = self.base.add('1')

        self.eq(self.base.get(1), item)
        self.eq(self.base.get('1'), item)
        self.eq(self.base['1'], item)
        self.eq(self.base[0], item)

        self.base.remove_all()

        item = self.base.add(1)
        self.eq(self.base.get(1), item)
        self.eq(self.base.get('1'), item)
        self.eq(self.base['1'], item)
        self.eq(self.base[0], item)

        for doc in self.base:
            self.eq(doc, item)

    def test_remove_item(self):
        self.base.add('1')
        self.base.remove('1')

        self.eq(self.base.get('1'), None)
        self.eq(self.base.get(1), None)
        self.eq(self.base['1'], None)

        self.base.add('1')
        self.base.remove(1)

        self.eq(self.base.get('1'), None)
        self.eq(self.base.get(1), None)
        self.eq(self.base['1'], None)

        self.base.add(1)
        self.base.remove(1)

        self.eq(self.base.get('1'), None)
        self.eq(self.base.get(1), None)
        self.eq(self.base['1'], None)

        self.base.add(1)
        self.base.remove('1')

        self.eq(self.base.get('1'), None)
        self.eq(self.base.get(1), None)
        self.eq(self.base['1'], None)

    def test_len(self):
        self.eq(self.base.length(), 0)

        self.base.add(1)
        self.base.add('1')
        self.eq(self.base.length(), 1)

        self.base.add(2)
        self.base.add('3')
        self.eq(self.base.length(), 3)

        self.base.remove(2)
        self.eq(self.base.get(2), None)
        self.base.remove('2')
        self.eq(self.base.length(), 2)

        self.base.remove_all()
        self.eq(self.base.length(), 0)

    def test_data(self):
        self.base.add(1)
        self.base.add(2)
        self.eq(self.base.data(), {'1': {}, '2': {}})

        item_list = self.base.add(3, list=True)
        self.isinstance(item_list, BaseList)
        self.eq(item_list.data(), [])
        self.eq(self.base.data(), {'1': {}, '2': {}, '3': []})

    def test_nested_list_data(self):
        self.base.add(1)
        l = self.base.add('d', list=True)
        ll = l.add(list=True)
        lll = ll.add()
        lll.add('sub1')
        lll.add('sub2')
        item1 = l.add()
        item2 = l.add()
        item1.add('item1')
        item2.add('item2')

        print self.base.data()

    def test_list(self):
        base_list = self.base.add(1, list=True)
        self.eq(base_list.name, '1')
        self.isinstance(base_list, BaseList)

        item0 = base_list.add()
        self.eq(base_list.length(), 1)
        self.eq(item0.name, '0')
        self.eq(base_list.get('0'), item0)
        self.eq(base_list.get(0), item0)
        self.isinstance(item0, Base)

        item1 = base_list.add(list=True)
        self.eq(base_list.length(), 2)
        self.eq(item1.name, '1')
        self.eq(base_list.get('1'), item1)
        self.eq(base_list.get(1), item1)
        self.isinstance(item1, BaseList)

        base_list.remove_all()
        self.eq(base_list.length(), 0)

        # remove
        item0 = base_list.add()
        item1 = base_list.add()
        item2 = base_list.add()
        item3 = base_list.add()
        self.eq(base_list.length(), 4)

        remove_item = base_list.remove(1)
        self.eq(remove_item, item1)
        self.eq(item0.name, '0')
        self.eq(item2.name, '1')
        self.eq(item3.name, '2')
        self.eq(item0, base_list.get(0))
        self.eq(item2, base_list.get(1))
        self.eq(item3, base_list.get(2))
        self.eq(None, base_list.get(3))
        self.eq(base_list.length(), 3)

        remove_item = base_list.remove(0)
        self.eq(remove_item, item0)
        self.eq(item2.name, '0')
        self.eq(item3.name, '1')
        self.eq(item2, base_list.get(0))
        self.eq(item3, base_list.get(1))
        self.eq(None, base_list.get(2))
        self.eq(base_list.length(), 2)

        self.eq(base_list.remove(2), None)
        self.eq(base_list.length(), 2)

        remove_item = base_list.remove(1)
        self.eq(remove_item, item3)
        self.eq(item2.name, '0')
        self.eq(item2, base_list.get(0))
        self.eq(None, base_list.get(1))
        self.eq(base_list.length(), 1)

        new_item = base_list.add()
        self.eq(new_item.name, '1')
        self.eq(base_list.get(1), new_item)
        self.eq(base_list.length(), 2)
