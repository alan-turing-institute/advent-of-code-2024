"""
Advent of Code 2024
Day 03
tomogwen
"""
from pathlib import Path
import re


if __name__ == "__main__":
    
    file_path = Path("input.txt")
    with open(file_path, 'r') as file:
        chars = file.read().strip()

    s = r"(mul\((\d+),(\d+)\)|don't|do)"
    groups  = re.findall(s, chars)

    part_one, part_two = 0, 0
    do = True
    for group in groups:
        if group[0] == "do":
            do = True
        elif group[0] == "don't":
            do = False
        else:
            result = int(group[1]) * int(group[2])
            part_one += result
            if do:
                part_two += result
    
    print("Part 1 solution:", part_one)
    print("Part 2 solution:", part_two)
