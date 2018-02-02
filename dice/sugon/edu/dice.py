import random


def roll(sides=6):
    """
    投掷一次骰子并返回点数。

    sides：骰子有多少面，默认为6。"""
    num_rolled = random.randint(1, sides)
    return num_rolled


def main():
    sides = 6
    stop = False
    while not stop:
        user_in = input('试试手气？ 回车=掷骰子， Q=退出')
        if user_in.lower() == 'q':
            stop = True
        else:
            num_rolled = roll(sides)
            print('你掷出了 %d 点' % num_rolled)
    print('欢迎下次再来')


if __name__ == '__main__':
    main()
