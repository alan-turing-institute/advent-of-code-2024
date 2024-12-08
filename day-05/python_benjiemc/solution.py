import sys
from itertools import permutations

import numpy as np


def check_update(update, rule_matrix):
    valid_update = True

    for idx, num in enumerate(update):
        for next_num in update[idx + 1:]:
            if rule_matrix[num, next_num]:
                valid_update = False
                break

        if not valid_update:
            break

    return valid_update


def part1(contents):
    rules, updates = contents.split('\n\n')

    rules = [(int(rule.split('|')[0]), int(rule.split('|')[1])) for rule in rules.split('\n') if rule]
    updates = [[int(num) for num in update.split(',')] for update in updates.split('\n') if update]

    size = max([val for rule in rules for val in rule])
    rule_matrix = np.zeros((size + 1, size + 1))
    for before, after in rules:
        rule_matrix[after, before] = 1

    total = 0
    for update in updates:
        if check_update(update, rule_matrix):
            total += update[len(update) // 2]

    return total


def swap_elements(i, j, update):
    """j > i"""
    item_i = update[i]
    item_j = update[j]

    return update[:i] + [item_j] + update[i + 1:j] + [item_i] + update[j + 1:]


def sort_update(update, rule_matrix):
    while not check_update(update, rule_matrix):
        for i in range(len(update)):
            for j in range(i, len(update)):
                if rule_matrix[update[i], update[j]]:
                    update = swap_elements(i, j, update)

    return update


def part2(contents):
    rules, updates = contents.split('\n\n')

    rules = [(int(rule.split('|')[0]), int(rule.split('|')[1])) for rule in rules.split('\n') if rule]
    updates = [[int(num) for num in update.split(',')] for update in updates.split('\n') if update]

    size = max([val for rule in rules for val in rule])
    rule_matrix = np.zeros((size + 1, size + 1))
    for before, after in rules:
        rule_matrix[after, before] = 1

    total = 0
    for update in updates:
        if not check_update(update, rule_matrix):
            new_update = sort_update(update, rule_matrix)
            total += new_update[len(new_update) // 2]

    return total


if __name__ == '__main__':
    with open(sys.argv[1]) as fh:
        contents = fh.read()

    print('Part 1 solution:', part1(contents))
    print('Part 2 solution:', part2(contents))
