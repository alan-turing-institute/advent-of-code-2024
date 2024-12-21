import sys

import functools


@functools.cache
def evaluate_design(design, patterns):
    if len(design) == 0:
        return True

    for pattern in patterns:
        if design.startswith(pattern):
            if evaluate_design(design[len(pattern):], patterns):
                return True

    return False


def part1(contents):
    patterns, potential_designs = contents.split('\n\n')

    patterns = tuple(patterns.split(', '))
    potential_designs = potential_designs.strip().split('\n')

    count = 0
    for design in potential_designs:
        if evaluate_design(design, patterns):
            count += 1

    return count


@functools.cache
def count_design(design, patterns):
    count = 0

    if len(design) == 0:
        return 1

    for pattern in patterns:
        if design.startswith(pattern):
            count += count_design(design[len(pattern):], patterns)

    return count


def part2(contents):
    patterns, potential_designs = contents.split('\n\n')

    patterns = tuple(patterns.split(', '))
    potential_designs = potential_designs.strip().split('\n')

    total = 0
    for design in potential_designs:
        total += count_design(design, patterns)

    return total


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as fh:
        contents = fh.read()

    print('Solution to part 1:', part1(contents))
    print('Solution to part 2:', part2(contents))
