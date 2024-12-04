"""
Advent of Code 2024
Day 04
tomogwen
"""
from pathlib import Path


def parse_file(file_path):
    grid = []
    with open(file_path, 'r') as file:
        for line in file:
            grid.append(list(line.strip()))
    return grid


def check_right(grid, word=['X', 'M', 'A', 'S']):
    count_internal = 0
    for row in grid:
        for j, letter in enumerate(row):
            if letter == 'X':
                if list(row[j:j+4]) == word:
                    count_internal += 1
    return count_internal


def check_down_right(grid):
    count_internal = 0
    for i, row in enumerate(grid):
        for j, letter in enumerate(row):
            if letter == 'X' and i < len(grid)-3 and j < len(row)-3:
                if grid[i+1][j+1] == 'M' and grid[i+2][j+2] == 'A' and grid[i+3][j+3] == 'S':
                    count_internal += 1
    return count_internal


def check_xmas(grid):
    count_internal = 0
    for i in range(1, len(grid)-1):
        for j in range(1, len(grid[0])-1):
            if grid[i][j] == 'A':
                if (grid[i-1][j-1] == 'M' and grid[i-1][j+1] == 'S' and grid[i+1][j-1] == 'M' and grid[i+1][j+1] == "S"):
                    count_internal += 1
    return count_internal


if __name__ == "__main__":
    file_path = Path('input.txt')
    grid = parse_file(file_path)

    part_one, part_two = 0, 0
    for i in range(4):
        part_one += check_right(grid)
        part_one += check_down_right(grid)
        part_two += check_xmas(grid)
        grid = list(zip(*reversed(grid)))  # rotate 90

    print("Part 1 solution:", part_one)
    print("Part 2 solution:", part_two)

