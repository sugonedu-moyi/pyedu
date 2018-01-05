# -*- coding: utf-8 -*-

import unittest
# from sugonedu.tree import pair, first, second, make_list, map_list, nil
from edu.tree.tree import pair, first, second, make_list, map_list, nil


class TestPair(unittest.TestCase):

    def test_pair(self):
        p = pair(1, 2)
        self.assertEqual(first(p), 1)
        self.assertEqual(second(p), 2)

    def test_make_list(self):
        ls = make_list(iter([1, 2, 3]))
        item1 = first(ls)
        item2 = first(second(ls))
        item3 = first(second(second(ls)))
        end = second(second(second(ls)))
        self.assertEqual(item1, 1)
        self.assertEqual(item2, 2)
        self.assertEqual(item3, 3)
        self.assertEqual(end, nil)

    def test_map_list(self):
        ls1 = make_list(iter([1, 2, 3]))
        ls2 = map_list(lambda x: x * 3, ls1)
        item1 = first(ls2)
        item2 = first(second(ls2))
        item3 = first(second(second(ls2)))
        end = second(second(second(ls2)))
        self.assertEqual(item1, 3)
        self.assertEqual(item2, 6)
        self.assertEqual(item3, 9)
        self.assertEqual(end, nil)


if __name__ == '__main__':
    unittest.main()
