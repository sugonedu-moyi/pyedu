# -*- coding: utf-8 -*-

"""buffer模块用于遍历token。"""

import math


class Buffer:
    """Buffer用于遍历多行token。

    例如：

    >>> buf = Buffer(iter([['(', '+'], [15], [12, ')']]))
    >>> buf.remove_front()
    '('
    >>> buf.remove_front()
    '+'
    >>> buf.current()
    15
    >>> print(buf)
    1: ( +
    2:  >> 15
    >>> buf.remove_front()
    15
    >>> buf.current()
    12
    >>> buf.remove_front()
    12
    >>> print(buf)
    1: ( +
    2: 15
    3: 12 >> )
    >>> buf.remove_front()
    ')'
    >>> print(buf)
    1: ( +
    2: 15
    3: 12 ) >>
    >>> buf.remove_front()  # 返回None
    """
    def __init__(self, source):
        """
        source是iterator。
        next(source)返回元素为token的list，对应一行文本。"""
        self.index = 0      # 当前行list的当前token的索引
        self.lines = []     # 已处理的行，包括当前行
        self.source = source
        self.current_line = ()
        self.current()

    def remove_front(self):
        """返回并移除当前token，不存在当前token则返回None。"""
        current = self.current()
        if current is not None:
            self.index += 1
        return current

    def current(self):
        """返回当前token或None。"""
        while not self.more_on_line():
            self.index = 0
            try:
                self.current_line = next(self.source)
                self.lines.append(self.current_line)
            except StopIteration:
                self.current_line = ()
                return None
        return self.current_line[self.index]

    def more_on_line(self):
        """当前行是否存在未处理的token。"""
        return self.index < len(self.current_line)

    def __str__(self):
        """返回已读的token，并使用>>标记当前token。"""
        n = len(self.lines)
        msg = '{0:>' + str(math.floor(math.log10(n))+1) + "}: "

        s = ''
        for i in range(max(0, n-4), n-1):
            s += msg.format(i+1) + ' '.join(map(str, self.lines[i])) + '\n'
        s += msg.format(n)
        s += ' '.join(map(str, self.current_line[:self.index]))
        s += ' >> '
        s += ' '.join(map(str, self.current_line[self.index:]))
        return s.strip()


# 用于访问用户输入历史记录
try:
    import readline
except ImportError:
    pass


class InputReader:
    """InputReader是iterable类型，用于提示用户输入。

    迭代器每次读入一行用户输入。"""
    def __init__(self, prompt):
        self.prompt = prompt

    def __iter__(self):
        while True:
            yield input(self.prompt)
            self.prompt = ' ' * len(self.prompt)

