# -*- coding: utf-8 -*-

"""该模块提供了两个函数，用于将字符串转化为token列表。

  * tokenize_line
  * tokenize_lines

token有下列几种：

  * 数字：使用int或float表示
  * 布尔类型
  * symbol（符号）：使用字符串表示
  * 分界符号：英文小括号、英文句点、英文单引号
"""

import string
import sys
import tokenize

_NUMERAL_STARTS = set(string.digits) | set('+-.')
_SYMBOL_CHARS = (set('!$%&*/:<=>?@^_~') | set(string.ascii_lowercase) |
                 set(string.ascii_uppercase) | _NUMERAL_STARTS)
_STRING_DELIMS = set('"')
_WHITESPACE = set(' \t\n\r')
_SINGLE_CHAR_TOKENS = set("()[]'`")
_TOKEN_END = _WHITESPACE | _SINGLE_CHAR_TOKENS | _STRING_DELIMS | {',', ',@'}
DELIMITERS = _SINGLE_CHAR_TOKENS | {'.', ',', ',@'}


def valid_symbol(s):
    """判断字符串s是否是有效的scheme符号。"""
    if len(s) == 0:
        return False
    for c in s:
        if c not in _SYMBOL_CHARS:
            return False
    return True


def next_candidate_token(line, k):
    """解析下一个token。"""
    while k < len(line):
        c = line[k]
        if c == ';':
            return None, len(line)
        elif c in _WHITESPACE:
            k += 1
        elif c in _SINGLE_CHAR_TOKENS:
            if c == ']':
                c = ')'
            if c == '[':
                c = '('
            return c, k+1
        elif c == '#':  # 布尔值：#t、#f
            return line[k:k+2], min(k+2, len(line))
        elif c == ',':  # ,@
            if k+1 < len(line) and line[k+1] == '@':
                return ',@', k+2
            return c, k+1
        elif c in _STRING_DELIMS:
            if k+1 < len(line) and line[k+1] == c:
                return c+c, k+2
            line_bytes = (bytes(line[k:], encoding='utf-8'),)
            gen = tokenize.tokenize(iter(line_bytes).__next__)
            next(gen)
            token = next(gen)
            if token.type != tokenize.STRING:
                raise ValueError("无效的字符串: {0}".format(token.string))
            return token.string, token.end[1]+k
        else:
            j = k
            while j < len(line) and line[j] not in _TOKEN_END:
                j += 1
            return line[k:j], min(j, len(line))
    return None, len(line)


def tokenize_line(line):
    """从一行字符串中解析出token列表。

    结果中不包含注释和空白字符。
    返回：list"""
    result = []
    text, i = next_candidate_token(line, 0)
    while text is not None:
        if text in DELIMITERS:
            result.append(text)
        elif text == '#t' or text.lower() == 'true':
            result.append(True)
        elif text == '#f' or text.lower() == 'false':
            result.append(False)
        elif text == 'nil':
            result.append(text)
        elif text[0] in _SYMBOL_CHARS:
            number = False
            if text[0] in _NUMERAL_STARTS:
                try:
                    result.append(int(text))
                    number = True
                except ValueError:
                    try:
                        result.append(float(text))
                        number = True
                    except ValueError:
                        pass
            if not number:
                if valid_symbol(text):
                    result.append(text.lower())
                else:
                    raise ValueError("无效的数字或符号: {0}".format(text))
        elif text[0] in _STRING_DELIMS:
            result.append(text)
        else:
            print("warning: 无效的token: {0}".format(text), file=sys.stderr)
            print("    ", line, file=sys.stderr)
            print(" " * (i+3), "^", file=sys.stderr)
        text, i = next_candidate_token(line, i)
    return result


def tokenize_lines(lines):
    """解析行字符串序列为token。

    返回：迭代器，每个元素是一个token列表，对应一行文本。"""
    return map(tokenize_line, lines)


