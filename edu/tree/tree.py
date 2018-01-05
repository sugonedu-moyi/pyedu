# -*- coding: utf-8 -*-

# 用于表现空链表
nil = []


def pair(a, b):
    """创建一个pair对象。"""
    return [a, b]


def first(pair_object):
    """获取pair对象的first部分。"""
    return pair_object[0]


def second(pair_object):
    """获取pair对象的second部分。"""
    return pair_object[1]


def make_list(iterator):
    """使用迭代器的元素创建链表。

    链表以pair对象为基础构造。"""
    try:
        item = next(iterator)
        '*** 在这里补充你的代码 ***'
        return pair(item, make_list(iterator))
    except StopIteration:
        return nil


def print_list(plist):
    """打印链表"""
    if plist == nil:
        print()
    else:
        print(str(first(plist)), end=' ')
        print_list(second(plist))


def map_list(fn, plist):
    """对链表plist的每个元素应用fn函数，并返回新的链表。"""
    if plist == nil:
        return nil
    else:
        new_item = fn(first(plist))
        '*** 在这里补充你的代码 ***'
        return pair(new_item, map_list(fn, second(plist)))

