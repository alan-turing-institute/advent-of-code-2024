import sys
from collections import defaultdict

import numpy as np


def part1(contents):
    lists = [line.split() for line in contents.split('\n') if line]

    list1 = [int(item[0]) for item in lists]
    list2 = [int(item[1]) for item in lists]

    list1_sorted = sorted(list1)
    list2_sorted = sorted(list2)

    return sum((np.abs(item2 - item1) for item1, item2 in zip(list1_sorted, list2_sorted)))


def part2(contents):
    lists = [line.split() for line in contents.split('\n') if line]

    list1 = [int(item[0]) for item in lists]
    list2 = [int(item[1]) for item in lists]

    list2_counts = defaultdict(lambda: 0)

    for item in list2:
        list2_counts[item] += 1

    return sum((item * list2_counts[item] for item in list1 if item in list2_counts))


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as fh:
        contents = fh.read()

    print('Part 1 solution:', part1(contents))
    print('Part 2 soluction:', part2(contents))
