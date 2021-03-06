# -*- coding: utf-8 -*-

"""该模块提供了一个用于解析计算器表达式的parser。"""

from sugon.edu.scheme_tokens import tokenize_lines, DELIMITERS
from sugon.edu.scheme_buffer import Buffer, InputReader, LineReader


class Nil:
    """用于表达scheme的nil或()"""
    def __repr__(self):
        return 'nil'

    def __str__(self):
        return '()'

    def __len__(self):
        return 0

    def map(self, fn):
        return self


nil = Nil()


class Pair:
    """Pair对象拥有first和second两个属性。

    用于构造scheme list的时候，second属性要么指向一个list，要么是nil。

    >>> s = Pair(1, Pair(2, nil))
    >>> s
    Pair(1, Pair(2, nil))
    >>> print(s)
    (1 2)
    >>> print(s.map(lambda x: x+4))
    (5 6)
    """
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __repr__(self):
        return 'Pair({0}, {1})'.format(
            repr(self.first), repr(self.second))

    def __str__(self):
        s = '(' + str(self.first)
        second = self.second
        while isinstance(second, Pair):
            s += ' ' + str(second.first)
            second = second.second
        if second is not nil:
            s += ' . ' + str(second)
        return s + ')'

    def __len__(self):
        n, second = 1, self.second
        while isinstance(second, Pair):
            n += 1
            second = second.second
        if second is not nil:
            raise TypeError('无效的list：' + str(self))
        return n

    def __eq__(self, p):
        if not isinstance(p, Pair):
            return False
        return self.first == p.first and self.second == p.second

    def map(self, fn):
        """list的每个元素应用函数fn，生成新的list。"""
        mapped = fn(self.first)
        if self.second is nil or isinstance(self.second, Pair):
            return Pair(mapped, self.second.map(fn))
        else:
            raise TypeError('无效的list：' + str(self))


def scheme_read(src_buf):
    """从token的buffer中读取下一个表达式。

    返回：
    * 基本表达式
        * nil
        * number
        * boolean
        * 符号（symbol）
    * 复合表达式
        pair构造的list（可嵌套，从而构成树）
    例如：
    >>> scheme_read(Buffer(tokenize_lines(['nil'])))
    nil
    >>> scheme_read(Buffer(tokenize_lines(['1'])))
    1
    >>> scheme_read(Buffer(tokenize_lines(['true'])))
    True
    >>> scheme_read(Buffer(tokenize_lines(['(+ 1 2)'])))
    Pair('+', Pair(1, Pair(2, nil)))
    """
    if src_buf.current() is None:
        raise EOFError
    val = src_buf.remove_front()  # 取得首个token
    if val == 'nil':
        return nil
    elif val == '(':
        # *** 问题1开始 ***
        '*** 在这里补充你的代码 ***'
        return read_tail(src_buf)
        # *** 问题1结束 ***
    elif val == "'":
        # *** 问题6开始 ***
        '*** 在这里补充你的代码 ***'
        exp = scheme_read(src_buf)
        return Pair("quote", Pair(exp, nil))
        # *** 问题6结束 ***
    elif val not in DELIMITERS:
        return val
    else:
        raise SyntaxError('不该在此出现的token: {0}'.format(val))


def read_tail(src_buf):
    """读取list表达式的剩余部分。

    例如：
    >>> read_tail(Buffer(tokenize_lines([')'])))
    nil
    >>> read_tail(Buffer(tokenize_lines(['2 3)'])))
    Pair(2, Pair(3, nil))
    """
    try:
        if src_buf.current() is None:
            raise SyntaxError('不完整的表达式')
        elif src_buf.current() == ')':
            src_buf.remove_front()
            return nil
        elif src_buf.current() == '.':
            src_buf.remove_front()
            second = scheme_read(src_buf)
            if src_buf.current() == ')':
                src_buf.remove_front()
                return second
            else:
                raise SyntaxError('无效的pair表达式')
        else:
            # *** 问题1开始 ***
            '*** 在这里补充你的代码 ***'
            first = scheme_read(src_buf)
            second = read_tail(src_buf)
            return Pair(first, second)
            # *** 问题1结束 ***
    except EOFError:
        raise SyntaxError('不完整的表达式')


def buffer_input(prompt='scm> '):
    """返回一个Buffer对象，从用户输入中获取token。"""
    return Buffer(tokenize_lines(InputReader(prompt)))


def buffer_lines(lines):
    """返回一个Buffer对象，从lines中获取token。"""
    input_lines = LineReader(lines)
    return Buffer(tokenize_lines(input_lines))


def read_line(line):
    """从一行字符串中读取Scheme表达式。"""
    return scheme_read(Buffer(tokenize_lines([line])))


def read_print_loop():
    """处理表达式的读入-打印-循环。"""
    while True:
        try:
            src = buffer_input('read> ')
            while src.more_on_line():
                expression = scheme_read(src)
                print('str :', expression)
                print('repr:', repr(expression))
        except (SyntaxError, ValueError) as err:
            print(type(err).__name__ + ':', err)
        except (KeyboardInterrupt, EOFError):  # <Control>-D
            print()
            return


if __name__ == '__main__':
    read_print_loop()
