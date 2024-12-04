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


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as fh:
        contents = fh.read()

    print('Part 1 soluiton:', part1(contents))
