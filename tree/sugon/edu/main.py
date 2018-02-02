# -*- coding: utf-8 -*-

import unittest
import sugon.edu.tree as t


class TestPair(unittest.TestCase):

    def test_pair(self):
        p = t.pair(1, 2)
        self.assertEqual(t.first(p), 1)
        self.assertEqual(t.second(p), 2)

    def test_make_list(self):
        ls = t.make_list(iter([1, 2, 3]))
        item1 = t.first(ls)
        item2 = t.first(t.second(ls))
        item3 = t.first(t.second(t.second(ls)))
        end = t.second(t.second(t.second(ls)))
        self.assertEqual(item1, 1)
        self.assertEqual(item2, 2)
        self.assertEqual(item3, 3)
        self.assertEqual(end, t.nil)

    def test_map_list(self):
        ls1 = t.make_list(iter([1, 2, 3]))
        ls2 = t.map_list(lambda x: x * 3, ls1)
        item1 = t.first(ls2)
        item2 = t.first(t.second(ls2))
        item3 = t.first(t.second(t.second(ls2)))
        end = t.second(t.second(t.second(ls2)))
        self.assertEqual(item1, 3)
        self.assertEqual(item2, 6)
        self.assertEqual(item3, 9)
        self.assertEqual(end, t.nil)

    def test_tree(self):
        # 使用list构造一颗树，存放下面的s表达式
        # (* 1 (+ 2 3) (+ 4 5 6))
        # 等价的中缀表达式为
        # 1 * (2 + 3) * (4 + 5 + 6)
        ls1 = t.make_list(iter(['+', 2, 3]))
        ls2 = t.make_list(iter(['+', 4, 5, 6]))
        exp_list = None
        '*** 在这里补充你的代码 ***'
        exp_list = t.make_list(iter(['*', 1, ls1, ls2]))
        self.assertEqual(t.first(exp_list), '*')
        self.assertEqual(t.first(t.second(exp_list)), 1)
        sub_ls_1 = t.first(t.second(t.second(exp_list)))
        self.assertEqual(t.first(sub_ls_1), '+')
        self.assertEqual(t.first(t.second(sub_ls_1)), 2)
        self.assertEqual(t.first(t.second(t.second(sub_ls_1))), 3)
        sub_ls_2 = t.first(t.second(t.second(t.second(exp_list))))
        self.assertEqual(t.first(sub_ls_2), '+')
        self.assertEqual(t.first(t.second(sub_ls_2)), 4)
        self.assertEqual(t.first(t.second(t.second(sub_ls_2))), 5)
        self.assertEqual(t.first(t.second(t.second(t.second(sub_ls_2)))), 6)


if __name__ == '__main__':
    unittest.main()
