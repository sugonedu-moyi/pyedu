# -*- coding: utf-8 -*-

"""Scheme语言解释器。"""

from sugon.edu.scheme_primitives import *
from sugon.edu.scheme_reader import *


def scheme_eval(expr, env):
    """在环境env中求值scheme表达式expr。

    >>> expr = read_line('(+ 2 2)')
    >>> expr
    Pair('+', Pair(2, Pair(2, nil)))
    >>> scheme_eval(expr, create_global_frame())
    4
    """
    # 基本表达式的求值
    if scheme_symbolp(expr):
        return env.lookup(expr)
    elif self_evaluating(expr):
        return expr

    # 复合表达式的求值
    if not scheme_listp(expr):
        raise SchemeError('无效的复合表达式: {0}'.format(str(expr)))
    first, rest = expr.first, expr.second
    if not scheme_symbolp(first):
        raise SchemeError('无效的复合表达式: {0}'.format(str(expr)))
    if first in SPECIAL_FORMS:  # 特殊形式
        return SPECIAL_FORMS[first](rest, env)
    else:  # 过程调用表达式
        # *** 问题4开始 ***
        '*** 在这里补充你的代码 ***'
        procedure = scheme_eval(first, env)
        check_procedure(procedure)
        return procedure.eval_call(rest, env)
        # *** 问题4结束 ***


def self_evaluating(expr):
    """表达式expr是否求值为自身"""
    return scheme_atomp(expr) or scheme_stringp(expr) or expr is None


def scheme_apply(procedure, args, env):
    """使用参数args在环境env中应用procedure过程。"""
    check_procedure(procedure)
    return procedure.apply(args, env)


def eval_all(expressions, env):
    """在环境env中求值expressions列表的每一个表达式，并返回最后一个表达式的值。"""
    # *** 问题10开始 ***
    '*** 修改下面的代码 ***'
    # return scheme_eval(expressions.first, env)
    rest = expressions
    result = None
    while rest != nil:
        exp = rest.first
        result = scheme_eval(exp, env)
        rest = rest.second
    return result
    # *** 问题10结束 ***


class Frame:
    """用于绑定Scheme符号和值，从而构成环境。"""

    def __init__(self, parent):
        """构造一个空的frame，parent指向父frame（可以是None）。"""
        self.bindings = {}
        self.parent = parent

    def __repr__(self):
        if self.parent is None:
            return '<Global Frame>'
        s = sorted(['{0}: {1}'.format(k, v) for k, v in self.bindings.items()])
        return '<{{{0}}} -> {1}>'.format(', '.join(s), repr(self.parent))

    def define(self, symbol, value):
        """在frame中绑定符号symbol和值value。"""
        # *** 问题2开始 ***
        '*** 在这里补充你的代码 ***'
        self.bindings[symbol] = value
        # *** 问题2结束 ***

    def lookup(self, symbol):
        """查找绑定到符号symbol上的值。

        如果找不到符号symbol，抛出SchemeError。"""
        # *** 问题2开始 ***
        '*** 在这里补充你的代码 ***'
        if symbol in self.bindings:
            return self.bindings[symbol]
        elif self.parent:
            return self.parent.lookup(symbol)
        # *** 问题2结束 ***
        raise SchemeError('符号未绑定: {0}'.format(symbol))

    def make_child_frame(self, formals, vals):
        """创建一个环境frame用于函数调用，它的parent指向self。

        在新建的frame中，将形式参数绑定到对应的值。
        formals: 形式参数，Scheme list
        vals: 对应的值，Scheme list

        例如：
        >>> env = create_global_frame()
        >>> formals, expressions = read_line('(a b c)'), read_line('(1 2 3)')
        >>> env.make_child_frame(formals, expressions)
        <{a: 1, b: 2, c: 3} -> <Global Frame>>
        """
        child = Frame(self)
        # *** 问题8开始 ***
        '*** 在这里补充你的代码 ***'
        if len(formals) != len(vals):
            raise SchemeError('形式参数和实际参数值不匹配: \n{1}\n{2}'.format(formals, vals))
        while formals != nil:
            name = formals.first
            val = vals.first
            child.define(name, val)
            formals = formals.second
            vals = vals.second
        # *** 问题8结束 ***
        return child


class Procedure:
    """Scheme过程的基类。"""

    def apply(self, args, env):
        """在参数列表args上应用自身过程，具体功能由子类实现。"""
        pass

    def eval_call(self, operands, env):
        """求值参数然后调用自身过程。

        operands: scheme表达式列表。
        在环境env中求值参数operands，然后使用求值结果作为参数调用自身过程。"""
        # *** 问题4开始 ***
        '*** 在这里补充你的代码 ***'
        args = operands.map(lambda exp: scheme_eval(exp, env))
        return self.apply(args, env)
        # *** 问题4结束 ***


def scheme_procedurep(x):
    """判断x是否scheme函数。"""
    return isinstance(x, Procedure)


class PrimitiveProcedure(Procedure):
    """Scheme基本过程。"""

    def __init__(self, fn, use_env=False, name='primitive'):
        """
        fn: 求值本过程所对应的Python函数
        use_env: 调用fn是否需要传递env参数
        name: 过程的名称
        """
        self.name = name
        self.fn = fn
        self.use_env = use_env

    def __str__(self):
        return '#[{0}]'.format(self.name)

    def apply(self, args, env):
        """在环境env中应用自身过程，参数args是一个Scheme的list。

        >>> env = create_global_frame()
        >>> plus = env.bindings['+']
        >>> twos = Pair(2, Pair(2, nil))
        >>> plus.apply(twos, env)
        4
        """
        if not scheme_listp(args):
            raise SchemeError('参数args不是一个list: {0}'.format(args))
        # Scheme list 转为 Python list
        python_args = []
        while args is not nil:
            python_args.append(args.first)
            args = args.second
        # *** 问题3开始 ***
        '*** 在这里补充你的代码 ***'
        if self.use_env:
            python_args.append(env)
        try:
            return self.fn(*python_args)
        except TypeError:
            raise SchemeError('调用{0}时传递了错误的参数：{1}'.format(
                self.name, str(args)))
        # *** 问题3结束 ***


class LambdaProcedure(Procedure):
    """用户自定义的函数过程。"""

    def __init__(self, formals, body, env):
        """
        formals: 形式参数列表
        body: 函数体，Scheme list
        env: 环境
        """
        self.formals = formals
        self.body = body
        self.env = env

    def apply(self, args, env):
        """使用参数args在环境env中应用自身函数。

        应用函数意味着求值函数体的所有表达式。 """
        new_env = self.make_call_frame(args, env)
        return eval_all(self.body, new_env)

    def make_call_frame(self, args, env):
        """创建一个新的Frame，从而构成新的环境，用于本次函数应用。

        同时，在新的环境的Frame中，将函数的形式参数绑定到对应的实际参数上。"""
        # *** 问题9开始 ***
        '*** 在这里补充你的代码 ***'
        return env.make_child_frame(self.formals, args)
        # *** 问题9结束 ***

    def __str__(self):
        return str(Pair('lambda', Pair(self.formals, self.body)))

    def __repr__(self):
        return 'LambdaProcedure({0}, {1}, {2})'.format(
            repr(self.formals), repr(self.body), repr(self.env))


def add_primitives(frame, funcs_and_names):
    for name, fn, proc_name in funcs_and_names:
        frame.define(name, PrimitiveProcedure(fn, name=proc_name))


# 下面的do_xxx_form系列函数，用于求值各种特殊形式。
# 函数的第一个参数是一个Scheme列表，列表已经去掉了特殊形式的标识符本身。
# 例如(define x 5)，传入do_define_form函数的第一个参数，是包含 x 5 两个元素的Scheme列表。
# 函数的第二个参数是求值的环境。

def do_define_form(expressions, env):
    """求值define特殊形式，返回所定义的符号（symbol）。"""
    check_form(expressions, 2)
    target = expressions.first
    if scheme_symbolp(target):
        check_form(expressions, 2, 2)
        # *** 问题5开始 ***
        '*** 在这里补充你的代码 ***'
        value_exp = expressions.second.first
        value = scheme_eval(value_exp, env)
        env.define(target, value)
        return target
        # *** 问题5结束 ***
    elif isinstance(target, Pair) and scheme_symbolp(target.first):
        # *** 问题开始 ***
        '*** 在这里补充你的代码 ***'
        # *** 问题结束 ***
    else:
        if isinstance(target, Pair):
            bad_target = target.first
        else:
            bad_target = target
        raise SchemeError('不是符号（symbol）: {0}'.format(bad_target))


def do_quote_form(expressions, env):
    """求值quote特殊形式。"""
    check_form(expressions, 1, 1)
    # *** 问题6开始 ***
    '*** 在这里补充你的代码 ***'
    return expressions.first
    # *** 问题6结束 ***


def do_begin_form(expressions, env):
    """求值begin特殊形式。"""
    check_form(expressions, 1)
    return eval_all(expressions, env)


def do_lambda_form(expressions, env):
    """求值lambda特殊形式。"""
    check_form(expressions, 2)
    formals = expressions.first
    check_formals(formals)
    # *** 问题7开始 ***
    '*** 在这里补充你的代码 ***'
    body = expressions.second
    return LambdaProcedure(formals, body, env)
    # *** 问题7结束 ***


def do_if_form(expressions, env):
    """求值if特殊形式。"""
    check_form(expressions, 2, 3)
    if scheme_truep(scheme_eval(expressions.first, env)):
        return scheme_eval(expressions.second.first, env)
    elif len(expressions) == 3:
        return scheme_eval(expressions.second.second.first, env)


def do_and_form(expressions, env):
    """求值and特殊形式。"""
    # *** 问题开始 ***
    '*** 在这里补充你的代码 ***'
    # *** 问题结束 ***


def do_or_form(expressions, env):
    """求值or特殊形式。"""
    # *** 问题开始 ***
    '*** 在这里补充你的代码 ***'
    # *** 问题结束 ***


def do_cond_form(expressions, env):
    """求值cond特殊形式。"""
    while expressions is not nil:
        clause = expressions.first
        check_form(clause, 1)
        if clause.first == 'else':
            test = True
            if expressions.second != nil:
                raise SchemeError('else must be last')
        else:
            test = scheme_eval(clause.first, env)
        if scheme_truep(test):
            # *** 问题开始 ***
            '*** 在这里补充你的代码 ***'
            # *** 问题结束 ***
        expressions = expressions.second


def do_let_form(expressions, env):
    """求值let特殊形式。"""
    check_form(expressions, 2)
    let_env = make_let_frame(expressions.first, env)
    return eval_all(expressions.second, let_env)


def make_let_frame(bindings, env):
    if not scheme_listp(bindings):
        raise SchemeError('bad bindings list in let form')
    # *** 问题开始 ***
    '*** 在这里补充你的代码 ***'
    # *** 问题结束 ***


SPECIAL_FORMS = {
    'and': do_and_form,
    'begin': do_begin_form,
    'cond': do_cond_form,
    'define': do_define_form,
    'if': do_if_form,
    'lambda': do_lambda_form,
    'let': do_let_form,
    'or': do_or_form,
    'quote': do_quote_form
}


def check_form(expr, min, max=float('inf')):
    """检查expr，确保expr是一个Scheme列表，并且列表长度在min和max之间。

    如果没有通过检查，抛出SchemeError。
    """
    if not scheme_listp(expr):
        raise SchemeError('无效的表达式：' + str(expr))
    length = len(expr)
    if length < min:
        raise SchemeError('表达式的参数个数过少')
    elif length > max:
        raise SchemeError('表达式的参数个数过多')


def check_formals(formals):
    """检查formals，确保它是一个有效的形式参数列表。

    一个有效的形式参数列表，是一个元素为符号（symbol）类型的Scheme列表。
    其中，每一个符号都是不相同的。
    如果没有通过检查，抛出SchemeError。
    """
    symbols = set()
    def check_and_add(symbol):
        if not scheme_symbolp(symbol):
            raise SchemeError('不是一个符号（symbol）: {0}'.format(symbol))
        if symbol in symbols:
            raise SchemeError('重复的符号（symbol）: {0}'.format(symbol))
        symbols.add(symbol)

    while isinstance(formals, Pair):
        check_and_add(formals.first)
        formals = formals.second


def check_procedure(procedure):
    """检查确保procedure是一个有效的Scheme过程。"""
    if not scheme_procedurep(procedure):
        raise SchemeError('{0} is not callable: {1}'.format(
            type(procedure).__name__.lower(), str(procedure)))


def scheme_map(fn, lst, env):
    check_type(fn, scheme_procedurep, 0, 'map')
    check_type(lst, scheme_listp, 1, 'map')
    return lst.map(lambda x: fn.apply(Pair(x, nil), env))


def scheme_filter(fn, lst, env):
    check_type(fn, scheme_procedurep, 0, 'filter')
    check_type(lst, scheme_listp, 1, 'filter')
    head, current = nil, nil
    while lst is not nil:
        item, lst = lst.first, lst.second
        if fn.apply(Pair(item, nil), env):
            if head is nil:
                head = Pair(item, nil)
                current = head
            else:
                current.second = Pair(item, nil)
                current = current.second
    return head


def scheme_reduce(fn, lst, env):
    check_type(fn, scheme_procedurep, 0, 'reduce')
    check_type(lst, lambda x: x is not nil, 1, 'reduce')
    check_type(lst, scheme_listp, 1, 'reduce')
    value, lst = lst.first, lst.second
    while lst is not nil:
        value = fn.apply(scheme_list(value, lst.first), env)
        lst = lst.second
    return value


# 读取-求值-打印 循环
def read_eval_print_loop(next_buffer, env, interactive=False):
    """读取表达式并求值，直到文件结束或者键盘中断。"""
    while True:
        try:
            src = next_buffer()
            while src.more_on_line():
                expression = scheme_read(src)
                result = scheme_eval(expression, env)
                if result is not None:
                    print(result)
        except (SchemeError, SyntaxError, ValueError, RuntimeError) as err:
            if (isinstance(err, RuntimeError) and
                'maximum recursion depth exceeded' not in getattr(err, 'args')[0]):
                raise
            elif isinstance(err, RuntimeError):
                print('Error: maximum recursion depth exceeded')
            else:
                print('Error:', err)
        except KeyboardInterrupt:  # <Control>-C
            print()
            print('KeyboardInterrupt')
            if not interactive:
                return
        except EOFError:  # <Control>-D, etc.
            print()
            return


def create_global_frame():
    """创建全局环境，其中包含Scheme语言的内置名字。"""
    env = Frame(None)
    env.define('eval',
               PrimitiveProcedure(scheme_eval, True, 'eval'))
    env.define('apply',
               PrimitiveProcedure(scheme_apply, True, 'apply'))
    env.define('procedure?',
               PrimitiveProcedure(scheme_procedurep, False, 'procedure?'))
    env.define('map',
               PrimitiveProcedure(scheme_map, True, 'map'))
    env.define('filter',
               PrimitiveProcedure(scheme_filter, True, 'filter'))
    env.define('reduce',
               PrimitiveProcedure(scheme_reduce, True, 'reduce'))
    env.define('undefined', None)
    add_primitives(env, PRIMITIVES)
    return env


def run():
    import argparse
    parser = argparse.ArgumentParser(description='Scheme解释器')
    parser.add_argument('file', nargs='?',
                        type=argparse.FileType('r'), default=None,
                        help='要运行的Scheme文件')
    args = parser.parse_args()
    if args.file is not None:
        lines = args.file.readlines()
        next_buffer = lambda: buffer_lines(lines)
        interactive = False
    else:
        next_buffer = buffer_input
        interactive = True
    read_eval_print_loop(next_buffer, create_global_frame(),
                         interactive=interactive)


if __name__ == '__main__':
    run()
