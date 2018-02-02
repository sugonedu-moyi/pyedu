# -*- coding: utf-8 -*-

# 用于表现空链表
nil = []


def pair(a, b):
    """创建一个pair对象。"""
    return [a, b]


def is_pair(p):
    """判断p是否pair对象。"""
    return isinstance(p, list) and len(p) == 2


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


# 输出不带最外层括号的列表字符串
# 例如：1 2 3
def __list_to_string(plist):
    if plist == nil:
        return ''
    else:
        item = first(plist)
        if is_pair(item):
            item_str = list_to_string(item)
        else:
            item_str = str(item)
        if second(plist) != nil:
            return item_str + ' ' + __list_to_string(second(plist))
        else:
            return item_str


def list_to_string(plist):
    """list转换为s表达式格式的字符串。

    示例输出：(1 2 3)"""
    return '(' + __list_to_string(plist) + ')'


def map_list(fn, plist):
    """对链表plist的每个元素应用fn函数，并返回新的链表。"""
    if plist == nil:
        return nil
    else:
        new_item = fn(first(plist))
        '*** 在这里补充你的代码 ***'
        return pair(new_item, map_list(fn, second(plist)))

