# -*- coding: utf-8 -*-

import random


def roll(sides=6):
    """
    投掷一次骰子并返回点数。

    sides：骰子有多少面，默认为6。"""
    num_rolled = None
    '*** 在这里补充你的代码 ***'
    '*** 随机产生1-6之间的整数 ***'
    '*** 提示，查阅random的randint函数的文档 ***'
    num_rolled = random.randint(1, sides)
    return num_rolled


def main():
    sides = 6
    stop = False
    '*** 在这里补充你的代码 ***'
    '*** 修改while循环的条件，使用stop变量控制循环的结束 ***'
    while not stop:
        user_in = input('试试手气？ 回车=掷骰子， Q=退出')
        '*** 在这里补充你的代码 ***'
        '*** 修改if的条件，根据用户的选择做决定 ***'
        '*** 注意，用户输入Q，无论大小写都可以退出 ***'
        if user_in.lower() == 'q':
            stop = True
        else:
            num_rolled = None
            '*** 在这里补充你的代码 ***'
            '*** 调用roll函数来掷骰子 ***'
            num_rolled = roll(sides)
            print('你掷出了 %d 点' % num_rolled)
    print('欢迎下次再来')


if __name__ == '__main__':
    main()
