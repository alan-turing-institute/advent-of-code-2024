import sys

import numpy as np


def part1(contents):
    WORD = 'XMAS'

    def get_sequence(direction, start_coord, grid):
        sequence = []
        for i in range(0, 4):
            coord = direction * i + start_coord

            if coord[0] >= grid.shape[0] or coord[0] < 0:
                break

            if coord[1] >= grid.shape[1] or coord[1] < 0:
                break

            sequence.append(grid[coord[0], coord[1]])

        return ''.join(sequence)

    def check_coord(coord, grid):
        count = 0
        for row_dir in -1, 0, 1:
            for col_dir in -1, 0, 1:
                if row_dir == col_dir == 0:
                    continue

                direction = np.array([row_dir, col_dir])

                if get_sequence(direction, coord, grid) == WORD:
                    count += 1

        return count

    grid = np.array([[char for char in line] for line in contents.split('\n') if line])
    count = 0
    for row_idx in range(grid.shape[0]):
        for col_idx in range(grid.shape[1]):
            coord = np.array([row_idx, col_idx])

            if grid[coord[0], coord[1]] == 'X':
                count += check_coord(coord, grid)

    return count


def part2(contents):
    def validate_coord(coord, grid):
        if coord[0] >= grid.shape[0] or coord[0] < 0:
            return False

        if coord[1] >= grid.shape[1] or coord[1] < 0:
            return False

        return True

    def check_coord(coord, grid):
        top_left = coord + np.array([-1, -1])
        top_right = coord + np.array([-1, 1])
        bottom_left = coord + np.array([1, -1])
        bottom_right = coord + np.array([1, 1])

        if not (validate_coord(top_left, grid)
                and validate_coord(top_right, grid)
                and validate_coord(bottom_left, grid)
                and validate_coord(bottom_right, grid)):
            return False

        diag1 = {grid[top_left[0], top_left[1]], grid[bottom_right[0], bottom_right[1]]}
        diag2 = {grid[top_right[0], top_right[1]], grid[bottom_left[0], bottom_left[1]]}

        return diag1 == diag2 == {'M', 'S'}

    grid = np.array([[char for char in line] for line in contents.split('\n') if line])
    count = 0
    for row_idx in range(grid.shape[0]):
        for col_idx in range(grid.shape[1]):
            coord = np.array([row_idx, col_idx])

            if grid[coord[0], coord[1]] == 'A':
                if check_coord(coord, grid):
                    count += 1

    return count


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as fh:
        contents = fh.read()

    print('Part 1 soluiton:', part1(contents))
    print('Part 2 soluiton:', part2(contents))
