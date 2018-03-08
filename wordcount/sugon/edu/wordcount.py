#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys


def process_line(line, word_to_count):
    for word in line.split():
        if word in word_to_count:
            word_to_count[word] += 1
        else:
            word_to_count[word] = 1


def word_count(path):
    word_to_count = {}
    with open(path) as f:
        for line in f:
            process_line(line, word_to_count)
    return word_to_count


def main(argv):
    if len(argv) != 2:
        print('Usage: wordcount <file-path>')
        sys.exit(1)
    else:
        word_dict = word_count(argv[1])
        for word, count in word_dict.items():
            print('%s: %d' % (word, count))


if __name__ == '__main__':
    main(sys.argv)
