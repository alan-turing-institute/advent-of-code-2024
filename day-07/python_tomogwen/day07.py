"""
Advent of Code 2024
Day 06
tomogwen
"""
import itertools
from pathlib import Path
from tqdm import tqdm


def parse_file(file_path):
    results = []
    nums = []
    with open(file_path, 'r') as file:
        for line in file:
            split = line.strip().split(": ")
            results.append(int(split[0]))
            nums.append([int(x) for x in split[1].split(' ')])
    return results, nums


def plus(a, b):
    return a + b


def times(a, b):
    return a*b


def concat(a: int, b: int) -> int:
    return int(str(a) + str(b))


def check_if_possible(result, nums, allowed_ops):
    for operations in itertools.product(allowed_ops, repeat=len(nums)-1):
        count = nums[0]
        for x, op in zip(nums[1:], operations):
            count = op(count, x)
        if count == result:
            return True
    return False


if __name__ == "__main__":
    file_path = Path("input.txt")
    results, nums_list = parse_file(file_path)

    part_one_ops = [plus, times]
    part_two_ops = [plus, times, concat]

    part_one, part_two = 0, 0
    for result, nums in tqdm(zip(results, nums_list), total=len(results)):
        # part one
        if check_if_possible(result, nums, allowed_ops=part_one_ops):
            part_one += result
        # part two
        if check_if_possible(result, nums, allowed_ops=part_two_ops):
            part_two += result

    print("Part 1 solution:", part_one)
    print("Part 2 solution:", part_two)
