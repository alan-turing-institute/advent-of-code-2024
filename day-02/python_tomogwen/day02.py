"""
Advent of Code 2024
Day 02
tomogwen
"""
from pathlib import Path


def check_safety(nums):
    if nums[0] > nums[1]:
        check = lambda a, b: a > b
    elif nums[0] < nums[1]:
        check = lambda a, b: a < b
    else:
        return False
    for a, b in zip(nums[:-1], nums[1:]):
        if not(check(a, b) and 1 <= abs(a-b) <= 3):
            return False
    return True


def check_safety_error(nums):
    for sublist in [nums[:i] + nums[i+1:] for i in range(len(nums))]:
        if check_safety(sublist):
            return True
    return False


if __name__ == "__main__":
    part_one, part_two = 0, 0
    file_path = Path('input.txt')
    with open(file_path, 'r') as file:
        for line in file:
            nums = [int(x) for x in line.strip().split(" ")]
            if check_safety(nums):
                part_one += 1
                part_two += 1
            else:
                part_two += check_safety_error(nums)

    print("Part 1 solution:", part_one)
    print("Part 2 solution:", part_two)
