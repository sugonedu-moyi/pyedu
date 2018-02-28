# -*- coding: utf-8 -*-

"""Scheme语言解释器。"""

from scheme_primitives import *
from scheme_reader import *


def scheme_eval(expr, env):
    """在环境env中求值scheme表达式expr。

    >>> expr = read_line('(+ 2 2)')
    >>> expr
    Pair('+', Pair(2, Pair(2, nil)))
    >>> scheme_eval(expr, create_global_frame())
    4
    """
    # 基本数据的求值
    if scheme_symbolp(expr):
        return env.lookup(expr)
    elif self_evaluating(expr):
        return expr

    # 复合数据的求值
    if not scheme_listp(expr):
        raise SchemeError('无效的list: {0}'.format(str(expr)))
    first, rest = expr.first, expr.second
    if scheme_symbolp(first) and first in SPECIAL_FORMS:
        return SPECIAL_FORMS[first](rest, env)
    else:
        # BEGIN PROBLEM 5
        "*** YOUR CODE HERE ***"
        # END PROBLEM 5


def self_evaluating(expr):
    """表达式expr是否求值为自身"""
    return scheme_atomp(expr) or scheme_stringp(expr) or expr is None


def scheme_apply(procedure, args, env):
    """使用参数args在环境env中应用procedure过程。"""
    check_procedure(procedure)
    return procedure.apply(args, env)


def eval_all(expressions, env):
    """在环境env中求值expressions列表的每一个表达式，并返回最后一个表达式的值。"""
    # BEGIN PROBLEM 8
    return scheme_eval(expressions.first, env)
    # END PROBLEM 8


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
        # *** 问题开始 ***
        '*** 在这里补充你的代码 ***'
        # *** 问题结束 ***

    def lookup(self, symbol):
        """Return the value bound to SYMBOL. Errors if SYMBOL is not found."""
        # BEGIN PROBLEM 3
        "*** YOUR CODE HERE ***"
        # END PROBLEM 3
        raise SchemeError('unknown identifier: {0}'.format(symbol))

    def make_child_frame(self, formals, vals):
        """创建一个局部的frame，它的parent指向self。

        formals: 形参，Scheme list
        vals: 对应的值，Scheme list

        例如：
        >>> env = create_global_frame()
        >>> formals, expressions = read_line('(a b c)'), read_line('(1 2 3)')
        >>> env.make_child_frame(formals, expressions)
        <{a: 1, b: 2, c: 3} -> <Global Frame>>
        """
        child = Frame(self)
        # BEGIN PROBLEM 11
        "*** YOUR CODE HERE ***"
        # END PROBLEM 11
        return child


class Procedure:
    """Scheme过程的基类。"""
    def eval_call(self, operands, env):
        """求值参数然后调用函数。

        在环境env中求值参数operands，然后使用求值结果作为参数调用自身函数。"""
        # BEGIN PROBLEM 5
        "*** YOUR CODE HERE ***"
        # END PROBLEM 5


def scheme_procedurep(x):
    """判断x是否scheme函数。"""
    return isinstance(x, Procedure)


class PrimitiveProcedure(Procedure):
    """Scheme基本函数。"""

    def __init__(self, fn, use_env=False, name='primitive'):
        self.name = name
        self.fn = fn
        self.use_env = use_env

    def __str__(self):
        return '#[{0}]'.format(self.name)

    def apply(self, args, env):
        """在环境env中应用自身函数，参数args是scheme的list。

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
        # BEGIN PROBLEM 4
        "*** YOUR CODE HERE ***"
        # END PROBLEM 4


class LambdaProcedure(Procedure):
    """lambda表达式或define特殊形式定义的函数过程。"""

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
        """Make a frame that binds my formal parameters to ARGS, a Scheme list
        of values, for a lexically-scoped call evaluated in environment ENV."""
        # BEGIN PROBLEM 12
        "*** YOUR CODE HERE ***"
        # END PROBLEM 12

    def __str__(self):
        return str(Pair('lambda', Pair(self.formals, self.body)))

    def __repr__(self):
        return 'LambdaProcedure({0}, {1}, {2})'.format(
            repr(self.formals), repr(self.body), repr(self.env))


def add_primitives(frame, funcs_and_names):
    """Enter bindings in FUNCS_AND_NAMES into FRAME, an environment frame,
    as primitive procedures. Each item in FUNCS_AND_NAMES has the form
    (NAME, PYTHON-FUNCTION, INTERNAL-NAME)."""
    for name, fn, proc_name in funcs_and_names:
        frame.define(name, PrimitiveProcedure(fn, name=proc_name))

#################
# Special Forms #
#################

# Each of the following do_xxx_form functions takes the cdr of a special form as
# its first argument---a Scheme list representing a special form without the
# initial identifying symbol (if, lambda, quote, ...). Its second argument is
# the environment in which the form is to be evaluated.

def do_define_form(expressions, env):
    """Evaluate a define form."""
    check_form(expressions, 2)
    target = expressions.first
    if scheme_symbolp(target):
        check_form(expressions, 2, 2)
        # BEGIN PROBLEM 6
        "*** YOUR CODE HERE ***"
        # END PROBLEM 6
    elif isinstance(target, Pair) and scheme_symbolp(target.first):
        # BEGIN PROBLEM 10
        "*** YOUR CODE HERE ***"
        # END PROBLEM 10
    else:
        bad_target = target.first if isinstance(target, Pair) else target
        raise SchemeError('non-symbol: {0}'.format(bad_target))

def do_quote_form(expressions, env):
    """Evaluate a quote form."""
    check_form(expressions, 1, 1)
    # BEGIN PROBLEM 7
    "*** YOUR CODE HERE ***"
    # END PROBLEM 7

def do_begin_form(expressions, env):
    """Evaluate a begin form."""
    check_form(expressions, 1)
    return eval_all(expressions, env)

def do_lambda_form(expressions, env):
    """Evaluate a lambda form."""
    check_form(expressions, 2)
    formals = expressions.first
    check_formals(formals)
    # BEGIN PROBLEM 9
    "*** YOUR CODE HERE ***"
    # END PROBLEM 9

def do_if_form(expressions, env):
    """Evaluate an if form."""
    check_form(expressions, 2, 3)
    if scheme_truep(scheme_eval(expressions.first, env)):
        return scheme_eval(expressions.second.first, env)
    elif len(expressions) == 3:
        return scheme_eval(expressions.second.second.first, env)

def do_and_form(expressions, env):
    """Evaluate a (short-circuited) and form."""
    # BEGIN PROBLEM 13
    "*** YOUR CODE HERE ***"
    # END PROBLEM 13

def do_or_form(expressions, env):
    """Evaluate a (short-circuited) or form."""
    # BEGIN PROBLEM 13
    "*** YOUR CODE HERE ***"
    # END PROBLEM 13

def do_cond_form(expressions, env):
    """Evaluate a cond form."""
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
            # BEGIN PROBLEM 14
            "*** YOUR CODE HERE ***"
            # END PROBLEM 14
        expressions = expressions.second

def do_let_form(expressions, env):
    """Evaluate a let form."""
    check_form(expressions, 2)
    let_env = make_let_frame(expressions.first, env)
    return eval_all(expressions.second, let_env)

def make_let_frame(bindings, env):
    """Create a child frame of ENV that contains the definitions given in
    BINDINGS. The Scheme list BINDINGS must have the form of a proper bindings
    list in a let expression: each item must be a list containing a symbol
    and a Scheme expression."""
    if not scheme_listp(bindings):
        raise SchemeError('bad bindings list in let form')
    # BEGIN PROBLEM 15
    "*** YOUR CODE HERE ***"
    # END PROBLEM 15


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

# Utility methods for checking the structure of Scheme programs

def check_form(expr, min, max=float('inf')):
    """Check EXPR is a proper list whose length is at least MIN and no more
    than MAX (default: no maximum). Raises a SchemeError if this is not the
    case.

    >>> check_form(read_line('(a b)'), 2)
    """
    if not scheme_listp(expr):
        raise SchemeError('badly formed expression: ' + str(expr))
    length = len(expr)
    if length < min:
        raise SchemeError('too few operands in form')
    elif length > max:
        raise SchemeError('too many operands in form')

def check_formals(formals):
    """Check that FORMALS is a valid parameter list, a Scheme list of symbols
    in which each symbol is distinct. Raise a SchemeError if the list of
    formals is not a well-formed list of symbols or if any symbol is repeated.

    >>> check_formals(read_line('(a b c)'))
    """
    symbols = set()
    def check_and_add(symbol):
        if not scheme_symbolp(symbol):
            raise SchemeError('non-symbol: {0}'.format(symbol))
        if symbol in symbols:
            raise SchemeError('duplicate symbol: {0}'.format(symbol))
        symbols.add(symbol)

    while isinstance(formals, Pair):
        check_and_add(formals.first)
        formals = formals.second

def check_procedure(procedure):
    """检查确保procedure是一个有效的Scheme过程。"""
    if not scheme_procedurep(procedure):
        raise SchemeError('{0} is not callable: {1}'.format(
            type(procedure).__name__.lower(), str(procedure)))


####################
# Extra Procedures #
####################

def scheme_map(fn, lst, env):
    check_type(fn, scheme_procedurep, 0, 'map')
    check_type(lst, scheme_listp, 1, 'map')
    return lst.map(lambda x: complete_eval(fn.apply(Pair(x, nil), env)))

def scheme_filter(fn, lst, env):
    check_type(fn, scheme_procedurep, 0, 'filter')
    check_type(lst, scheme_listp, 1, 'filter')
    head, current = nil, nil
    while lst is not nil:
        item, lst = lst.first, lst.second
        if complete_eval(fn.apply(Pair(item, nil), env)):
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
        value = complete_eval(fn.apply(scheme_list(value, lst.first), env))
        lst = lst.second
    return value

################
# Input/Output #
################

def read_eval_print_loop(next_line, env, interactive=False, quiet=False,
                         startup=False, load_files=()):
    """Read and evaluate input until an end of file or keyboard interrupt."""
    if startup:
        for filename in load_files:
            scheme_load(filename, True, env)
    while True:
        try:
            src = next_line()
            while src.more_on_line():
                expression = scheme_read(src)
                result = scheme_eval(expression, env)
                if not quiet and result is not None:
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
            if not startup:
                raise
            print()
            print('KeyboardInterrupt')
            if not interactive:
                return
        except EOFError:  # <Control>-D, etc.
            print()
            return

def scheme_load(*args):
    """Load a Scheme source file. ARGS should be of the form (SYM, ENV) or
    (SYM, QUIET, ENV). The file named SYM is loaded into environment ENV,
    with verbosity determined by QUIET (default true)."""
    if not (2 <= len(args) <= 3):
        expressions = args[:-1]
        raise SchemeError('"load" given incorrect number of arguments: '
                          '{0}'.format(len(expressions)))
    sym = args[0]
    quiet = args[1] if len(args) > 2 else True
    env = args[-1]
    if (scheme_stringp(sym)):
        sym = eval(sym)
    check_type(sym, scheme_symbolp, 0, 'load')
    with scheme_open(sym) as infile:
        lines = infile.readlines()
    args = (lines, None) if quiet else (lines,)
    def next_line():
        return buffer_lines(*args)

    read_eval_print_loop(next_line, env, quiet=quiet)

def scheme_open(filename):
    """If either FILENAME or FILENAME.scm is the name of a valid file,
    return a Python file opened to it. Otherwise, raise an error."""
    try:
        return open(filename)
    except IOError as exc:
        if filename.endswith('.scm'):
            raise SchemeError(str(exc))
    try:
        return open(filename + '.scm')
    except IOError as exc:
        raise SchemeError(str(exc))

def create_global_frame():
    """创建全局环境，其中包含Scheme语言的内置名字。"""
    env = Frame(None)
    env.define('eval',
               PrimitiveProcedure(scheme_eval, True, 'eval'))
    env.define('apply',
               PrimitiveProcedure(scheme_apply, True, 'apply'))
    env.define('load',
               PrimitiveProcedure(scheme_load, True, 'load'))
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


def run(*argv):
    import argparse
    parser = argparse.ArgumentParser(description='Scheme Interpreter')
    parser.add_argument('-load', '-i', action='store_true',
                       help='run file interactively')
    parser.add_argument('file', nargs='?',
                        type=argparse.FileType('r'), default=None,
                        help='Scheme file to run')
    args = parser.parse_args()

    next_line = buffer_input
    interactive = True
    load_files = []

    if args.file is not None:
        if args.load:
            load_files.append(getattr(args.file, 'name'))
        else:
            lines = args.file.readlines()
            def next_line():
                return buffer_lines(lines)
            interactive = False

    read_eval_print_loop(next_line, create_global_frame(), startup=True,
                         interactive=interactive, load_files=load_files)


if __name__ == '__main__':
    import sys
    run(sys.argv)
