"""
Advent of Code 2024
Day 05
tomogwen
"""
from functools import cmp_to_key, partial
from math import floor
from pathlib import Path


def parse_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    rules = [[int(x) for x in line.strip().split("|")] for line in lines if "|" in line]
    updates = [[int(x) for x in line.strip().split(",")] for line in lines if "," in line]

    return rules, updates


def custom_order(x, y, rules):
    # Return negative if x < y, zero if x == y, positive if x > y
    if x == y:
        return 0
    elif [x, y] in rules:
        return -1
    else:
        return 1


if __name__ == "__main__":
    file_path = Path("input.txt")
    rules, updates = parse_file(file_path)

    # define custom order using comparisons
    order = partial(custom_order, rules=rules)
    sorted_custom = partial(sorted, key=cmp_to_key(order))
    
    part_one, part_two = 0, 0
    for update in updates:
        idx = floor(len(update)/2)
        sorted_pages = sorted_custom(update)
        if sorted_pages == update:
            part_one += update[idx]
        else:
            part_two += sorted_pages[idx]
    
    print("Part 1 solution:", part_one)
    print("Part 2 solution:", part_two)
