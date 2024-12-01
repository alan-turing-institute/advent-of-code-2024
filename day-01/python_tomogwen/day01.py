"""
Advent of Code 2024
Day 01
tomogwen
"""

from pathlib import Path
from typing import List, Tuple


def parse_file(file_path: Path) -> Tuple[List[int], List[int]]:
    """Maps file into a list of left-hand side and list of right-hand side numbers."""
    left, right = [], []
    with open(file_path, 'r') as file:
        for line in file:
            nums = line.strip().split("   ")
            left.append(int(nums[0]))
            right.append(int(nums[1]))

    return left, right


def part_one(left: List[int], right: List[int]) -> int:
    """Solves part one."""
    total = 0
    for l, r in zip(sorted(left), sorted(right)):
        total += abs(l - r)
    return total


def part_two(left: List[int], right: List[int]) -> int:
    """Solves part two."""
    counts = {}
    for r in right:
        if r not in counts.keys():
            counts[r] = 1
        else:
            counts[r] += 1

    total = 0
    for l in left:
        if l in counts.keys():
            total += l * counts[l]
    
    return total


if __name__ == "__main__":
    
    file_path = Path('input.txt')
    left, right = parse_file(file_path)

    solution_one = part_one(left, right)
    print("Part 1 solution:", solution_one)

    solution_two = part_two(left, right)
    print("Part 2 solution:", solution_two)
