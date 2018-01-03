import random


def is_valid_number(s):
    """判断字符串s是否表示有效的数字"""
    return s.isdigit() and 1 <= int(s) <= 100


def main():
    # 生成要猜的数字
    number = random.randint(1, 100)
    # 是否猜对了
    guess_ok = False
    # 猜数字的次数
    num_guesses = 0
    guess_str = input('请猜一个1-100之间的数字：')
    while not guess_ok:
        if is_valid_number(guess_str):
            num_guesses += 1
            guess = int(guess_str)
            if guess < number:
                guess_str = input('太小了。再猜一次：')
            elif guess > number:
                guess_str = input('太大了。再猜一次：')
            else:
                guess_ok = True
                print('猜对了！一共猜了 %d 次' % num_guesses)
        else:
            guess_str = input('输入无效。请猜一个1-100之间的数字：')


if __name__ == '__main__':
    main()
