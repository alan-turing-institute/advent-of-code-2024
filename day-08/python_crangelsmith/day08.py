import os
import numpy as np

import itertools


def parse_file(file_path):
    with open(os.path.join(file_path)) as f:
        lines = f.read().splitlines()
    return np.array([[char for char in l] for l in lines])

def check_bounds(position, bounds):

    if position[0] < 0 or position[1] < 0 or position[0] > bounds[0] or position[1] > bounds[1]:
        return False

    return True

def check_antinode(a0, a1, diff1, diff2, data_bounds, antinodes):
    updated_antinodes = antinodes.copy()

    a0_new = (a0[0] + diff1, a0[1] + diff2)
    a1_new = (a1[0] - diff1, a1[1] - diff2)

    if check_bounds(a0_new, data_bounds):
        updated_antinodes.append(a0_new)
    if check_bounds(a1_new, data_bounds):
        updated_antinodes.append(a1_new)

    return updated_antinodes


if __name__ == "__main__":

    import time

    time_start1 = time.time()
    file_name = "test8.txt"
    file_name = "input_day8.txt"


    data = parse_file(file_name)

    unique_antennas = set(data.flatten()) - {'.', '#'}


    antinodes_part1 = []
    antinodes_par2 = []

    bounds = (data.shape[0] - 1, data.shape[1] - 1)

    for i in unique_antennas:

        positions = np.argwhere(data == i)

        antenna_positions = list(zip(positions[0], positions[1]))
        pairs = list(itertools.combinations(antenna_positions, 2))

        for a0, a1 in pairs:

            diff1 = a0[0] - a1[0]
            diff2 = a0[1] - a1[1]

            antinodes_part1 = check_antinode(a0, a1, diff1, diff2, bounds, antinodes_part1)

            # Part 2
            antinodes_par2.append(a0)
            antinodes_par2.append(a1)

            while True:

                new_antinodes = check_antinode(a0, a1, diff1, diff2, bounds, antinodes_par2)

                if antinodes_par2 == new_antinodes:
                    break

                else:
                    antinodes_par2 = new_antinodes
                    a0 = (a0[0] + diff1, a0[1] + diff2)
                    a1 = (a1[0] - diff1, a1[1] - diff2)

    print("Solution to part1: ", len(set(antinodes_part1)))
    print("Solution to part1: ", len(set(antinodes_par2)))

    time_end1 = time.time()
    print("Time taken for Part 1: ", time_end1 - time_start1)