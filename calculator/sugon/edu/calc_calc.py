# -*- coding: utf-8 -*-

"""Scheme语法（S表达式）计算器的求值。

一些例子:
    > (* 1 2 3)
    6
    > (+)
    0
    > (+ 2 (/ 4 8))
    2.5
    > (+ 2 2) (* 3 3)
    4
    9
    > (+ 1
         (- 23)
         (* 4 2.5))
    -12
    > )
    SyntaxError: 不该在此出现的token: )
    > 2.3.4
    ValueError: 不是一个数字或可调用表达式
    > +
    TypeError: + 不是一个数字或可调用表达式
    > (/ 1 0)
    ZeroDivisionError: division by zero
"""

from operator import add, sub, mul, truediv
from sugon.edu.calc_reader import Pair, nil, scheme_read, buffer_input


def calc_eval(exp):
    """求值计算器表达式exp。

    示例：
    >>> calc_eval(as_scheme_list('+', 2, as_scheme_list('*', 4, 6)))
    26
    >>> calc_eval(as_scheme_list('+', 2, as_scheme_list('/', 40, 5)))
    10
    """
    if type(exp) in (int, float):
        return simplify(exp)
    elif isinstance(exp, Pair):
        arguments = None
        # *** 问题4开始 ***
        '*** 在这里补充你的代码 ***'
        arguments = exp.second.map(calc_eval)
        # *** 问题4结束 ***
        value = calc_apply(exp.first, arguments)
        return simplify(value)
    else:
        raise TypeError(str(exp) + ' 不是一个数字或可调用表达式')


def calc_apply(operator, args):
    """在args参数列表上应用operator操作符。

    示例：
    >>> calc_apply('+', as_scheme_list(1, 2, 3))
    6
    >>> calc_apply('-', as_scheme_list(10, 1, 2, 3))
    4
    >>> calc_apply('-', as_scheme_list(10))
    -10
    >>> calc_apply('*', nil)
    1
    >>> calc_apply('*', as_scheme_list(1, 2, 3, 4, 5))
    120
    >>> calc_apply('/', as_scheme_list(40, 5))
    8.0
    >>> calc_apply('/', as_scheme_list(10))
    0.1
    """
    if not isinstance(operator, str):
        raise TypeError(str(operator) + ' 不是一个符号')
    if operator == '+':
        return plist_reduce(add, args, 0)
    elif operator == '-':
        if len(args) == 0:
            raise TypeError(operator + ' 需要至少一个参数')
        elif len(args) == 1:
            return -args.first
        else:
            return plist_reduce(sub, args.second, args.first)
    elif operator == '*':
        # *** 问题5开始 ***
        '*** 在这里补充你的代码 ***'
        return plist_reduce(mul, args, 1)
        # *** 问题5结束 ***
    elif operator == '/':
        if len(args) == 0:
            raise TypeError(operator + ' 需要至少一个参数')
        elif len(args) == 1:
            return 1/args.first
        else:
            return plist_reduce(truediv, args.second, args.first)
    else:
        raise TypeError(operator + ' 是一个未知的操作符')


def simplify(value):
    """如果value是float类型并且是整数则转换为int类型，否则返回value本身。

    >>> simplify(8.0)
    8
    >>> simplify(2.3)
    2.3
    >>> simplify('+')
    '+'
    """
    if isinstance(value, float) and int(value) == value:
        return int(value)
    return value


def plist_reduce(fn, scheme_list, start):
    """pair节点链表的reduce实现。

    >>> plist_reduce(add, as_scheme_list(1, 2, 3), 0)
    6
    """
    if scheme_list is nil:
        return start
    return plist_reduce(fn, scheme_list.second, fn(start, scheme_list.first))


def as_scheme_list(*args):
    """将函数参数作为元素构造pair为节点的链表。

    >>> as_scheme_list(1, 2, 3)
    Pair(1, Pair(2, Pair(3, nil)))
    """
    if len(args) == 0:
        return nil
    return Pair(args[0], as_scheme_list(*args[1:]))


def read_eval_print_loop():
    """运行计算器的"读取-求值-打印"循环。"""
    while True:
        try:
            src = buffer_input()
            while src.more_on_line():
                expression = scheme_read(src)
                value = calc_eval(expression)
                print(value)
        except (SyntaxError, TypeError, ValueError, ZeroDivisionError) as err:
            print(type(err).__name__ + ':', err)
        except (KeyboardInterrupt, EOFError):  # <Control>-D等特殊按键
            print('计算完毕。')
            return


if __name__ == '__main__':
    read_eval_print_loop()
