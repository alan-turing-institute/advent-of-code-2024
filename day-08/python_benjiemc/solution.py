import itertools
import math
import sys

import numpy as np


def in_bounds(coord, shape):
    return coord[0] >= 0 and coord[0] < shape[0] and coord[1] >= 0 and coord[1] < shape[1]


def part1(contents):
    grid = np.array([[element for element in line] for line in contents.split('\n') if line])
    antenna_types = [el for el in np.unique(grid) if el != '.']

    antinodes = set([])

    for antenna_type in antenna_types:

        antenna_coords = []
        for row_coord in range(grid.shape[0]):
            for col_coord in range(grid.shape[1]):
                if grid[row_coord, col_coord] == antenna_type:
                    antenna_coords.append(np.array([row_coord, col_coord]))

        for ant1_coord, ant2_coord in itertools.combinations(antenna_coords, 2):
            direction = ant2_coord - ant1_coord

            anti_node1 = ant2_coord + direction
            anti_node2 = ant1_coord - direction

            if in_bounds(anti_node1, grid.shape):
                antinodes.add((anti_node1[0], anti_node1[1]))

            if in_bounds(anti_node2, grid.shape):
                antinodes.add((anti_node2[0], anti_node2[1]))

    return len(antinodes)


def part2(contents):
    grid = np.array([[element for element in line] for line in contents.split('\n') if line])
    antenna_types = [el for el in np.unique(grid) if el != '.']

    antinodes = set([])

    for antenna_type in antenna_types:

        antenna_coords = []
        for row_coord in range(grid.shape[0]):
            for col_coord in range(grid.shape[1]):
                if grid[row_coord, col_coord] == antenna_type:
                    antenna_coords.append(np.array([row_coord, col_coord]))

        for ant1_coord, ant2_coord in itertools.combinations(antenna_coords, 2):
            direction = ant2_coord - ant1_coord
            direction = direction / math.gcd(direction[0], direction[1])

            antinode = ant1_coord

            while in_bounds(antinode, grid.shape):
                antinodes.add((antinode[0], antinode[1]))
                antinode = antinode + direction

            antinode = ant1_coord

            while in_bounds(antinode, grid.shape):
                antinodes.add((antinode[0], antinode[1]))
                antinode = antinode - direction

    return len(antinodes)


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as fh:
        contents = fh.read()

    print('Part 1 solution:', part1(contents))
    print('Part 2 solution:', part2(contents))
