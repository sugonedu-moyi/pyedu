# coding: utf-8

"""本模块实现了Scheme语言的基本操作过程。"""

import math
import operator
import sys
from sugon.edu.scheme_reader import Pair, nil


class SchemeError(Exception):
    """用于表示Scheme程序中的错误。"""


# 每个元素是一个三元组：(名字，对应的python函数，内部名字)
# 通过primitive装饰器添加
# 在scheme模块的create_global_frame中使用
PRIMITIVES = []


# 定义装饰器
def primitive(*names):
    def add(fn):
        for name in names:
            PRIMITIVES.append((name, fn, names[0]))
        return fn
    return add


def check_type(val, predicate, k, name):
    if not predicate(val):
        msg = "argument {0} of {1} has wrong type ({2})"
        raise SchemeError(msg.format(k, name, type(val).__name__))
    return val


@primitive("boolean?")
def scheme_booleanp(x):
    return x is True or x is False


def scheme_truep(val):
    return val is not False


def scheme_falsep(val):
    return val is False


@primitive("not")
def scheme_not(x):
    return not scheme_truep(x)


@primitive("equal?")
def scheme_equalp(x, y):
    if scheme_pairp(x) and scheme_pairp(y):
        return scheme_equalp(x.first, y.first) and scheme_equalp(x.second, y.second)
    elif scheme_numberp(x) and scheme_numberp(y):
        return x == y
    else:
        return type(x) == type(y) and x == y


@primitive("eq?")
def scheme_eqp(x, y):
    if scheme_numberp(x) and scheme_numberp(y):
        return x == y
    elif scheme_symbolp(x) and scheme_symbolp(y):
        return x == y
    else:
        return x is y


@primitive("pair?")
def scheme_pairp(x):
    return isinstance(x, Pair)


@primitive("null?")
def scheme_nullp(x):
    return x is nil


@primitive("list?")
def scheme_listp(x):
    while x is not nil:
        if not isinstance(x, Pair):
            return False
        x = x.second
    return True


@primitive("length")
def scheme_length(x):
    check_type(x, scheme_listp, 0, 'length')
    if x is nil:
        return 0
    return len(x)


@primitive("cons")
def scheme_cons(x, y):
    return Pair(x, y)


@primitive("car")
def scheme_car(x):
    check_type(x, scheme_pairp, 0, 'car')
    return x.first


@primitive("cdr")
def scheme_cdr(x):
    check_type(x, scheme_pairp, 0, 'cdr')
    return x.second


@primitive("list")
def scheme_list(*vals):
    result = nil
    for e in reversed(vals):
        result = Pair(e, result)
    return result


@primitive("append")
def scheme_append(*vals):
    if len(vals) == 0:
        return nil
    result = vals[-1]
    for i in range(len(vals)-2, -1, -1):
        v = vals[i]
        if v is not nil:
            check_type(v, scheme_pairp, i, 'append')
            r = p = Pair(v.first, result)
            v = v.second
            while scheme_pairp(v):
                p.second = Pair(v.first, result)
                p = p.second
                v = v.second
            result = r
    return result


@primitive("string?")
def scheme_stringp(x):
    return isinstance(x, str) and x.startswith('"')


@primitive("symbol?")
def scheme_symbolp(x):
    return isinstance(x, str) and not scheme_stringp(x)


@primitive("number?")
def scheme_numberp(x):
    return isinstance(x, (int, float)) and not scheme_booleanp(x)


@primitive("integer?")
def scheme_integerp(x):
    return scheme_numberp(x) and (isinstance(x, int) or round(x) == x)


def _check_nums(*vals):
    """检查确保vals中的所有参数都是数字。"""
    for i, v in enumerate(vals):
        if not scheme_numberp(v):
            msg = "operand {0} ({1}) is not a number"
            raise SchemeError(msg.format(i, v))


def _arith(fn, init, vals):
    _check_nums(*vals)
    s = init
    for val in vals:
        s = fn(s, val)
    if round(s) == s:
        s = round(s)
    return s


@primitive("+")
def scheme_add(*vals):
    return _arith(operator.add, 0, vals)


@primitive("-")
def scheme_sub(val0, *vals):
    _check_nums(val0, *vals) # fixes off-by-one error
    if len(vals) == 0:
        return -val0
    return _arith(operator.sub, val0, vals)


@primitive("*")
def scheme_mul(*vals):
    return _arith(operator.mul, 1, vals)


@primitive("/")
def scheme_div(val0, *vals):
    _check_nums(val0, *vals) # fixes off-by-one error
    try:
        if len(vals) == 0:
            return 1 / val0
        return _arith(operator.truediv, val0, vals)
    except ZeroDivisionError as err:
        raise SchemeError(err)


@primitive("expt")
def scheme_expt(val0, val1):
    _check_nums(val0, val1)
    return pow(val0, val1)


@primitive("abs")
def scheme_abs(val0):
    return abs(val0)


@primitive("quotient")
def scheme_quo(val0, val1):
    _check_nums(val0, val1)
    try:
        return int(val0 / val1)
    except ZeroDivisionError as err:
        raise SchemeError(err)


@primitive("modulo")
def scheme_modulo(val0, val1):
    _check_nums(val0, val1)
    try:
        return val0 % val1
    except ZeroDivisionError as err:
        raise SchemeError(err)


@primitive("remainder")
def scheme_remainder(val0, val1):
    _check_nums(val0, val1)
    try:
        result = val0 % val1
    except ZeroDivisionError as err:
        raise SchemeError(err)
    while result < 0 and val0 > 0 or result > 0 and val0 < 0:
        result -= val1
    return result


def number_fn(module, name):
    py_fn = getattr(module, name)
    def scheme_fn(*vals):
        _check_nums(*vals)
        return py_fn(*vals)
    return scheme_fn


for _name in ["acos", "acosh", "asin", "asinh", "atan", "atan2", "atanh",
              "ceil", "copysign", "cos", "cosh", "degrees", "floor", "log",
              "log10", "log1p", "log2", "radians", "sin", "sinh", "sqrt",
              "tan", "tanh", "trunc"]:
    primitive(_name)(number_fn(math, _name))


def _numcomp(op, x, y):
    _check_nums(x, y)
    return op(x, y)


@primitive("=")
def scheme_eq(x, y):
    return _numcomp(operator.eq, x, y)


@primitive("<")
def scheme_lt(x, y):
    return _numcomp(operator.lt, x, y)


@primitive(">")
def scheme_gt(x, y):
    return _numcomp(operator.gt, x, y)


@primitive("<=")
def scheme_le(x, y):
    return _numcomp(operator.le, x, y)


@primitive(">=")
def scheme_ge(x, y):
    return _numcomp(operator.ge, x, y)


@primitive("even?")
def scheme_evenp(x):
    _check_nums(x)
    return x % 2 == 0


@primitive("odd?")
def scheme_oddp(x):
    _check_nums(x)
    return x % 2 == 1


@primitive("zero?")
def scheme_zerop(x):
    _check_nums(x)
    return x == 0


@primitive("atom?")
def scheme_atomp(x):
    return (scheme_booleanp(x) or scheme_numberp(x) or
            scheme_symbolp(x) or scheme_nullp(x))


@primitive("display")
def scheme_display(val):
    if scheme_stringp(val):
        val = eval(val)
    print(str(val), end="")


@primitive("print")
def scheme_print(val):
    print(str(val))


@primitive("newline")
def scheme_newline():
    print()
    sys.stdout.flush()


@primitive("error")
def scheme_error(msg=None):
    msg = "" if msg is None else str(msg)
    raise SchemeError(msg)


@primitive("exit")
def scheme_exit():
    raise EOFError
