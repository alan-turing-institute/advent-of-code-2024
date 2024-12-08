import numpy as np
from itertools import product, permutations
from collections import defaultdict

with open("input.txt") as file:
    input = file.read()

city_map = np.array(list(map(list, input.splitlines())))

EMPTY = "."


# PART ONE

antennas = defaultdict(list)  # frequency: locations
antinode_map = np.zeros_like(city_map, dtype=bool)

for loc in product(*map(range, city_map.shape)):
    frequency = city_map[loc]
    if frequency != EMPTY:
        for antenna_loc in antennas[frequency]:
            direction = np.subtract(antenna_loc, loc)
            antinode_locs = [antenna_loc + direction, loc - direction]
            for antinode_loc in antinode_locs:
                if np.all((antinode_loc >= 0) & (antinode_loc < city_map.shape)):
                    antinode_map[tuple(antinode_loc)] = True
        antennas[frequency].append(loc)

answer = antinode_map.sum()
print("Part One:", answer)


# PART TWO

# we already have the antennas locations
for locations in antennas.values():
    for loc1, loc2 in permutations(locations, r=2):
        direction = np.subtract(loc1, loc2)
        antinode_loc = np.array(loc1)
        while np.all((antinode_loc >= 0) & (antinode_loc < city_map.shape)):
            antinode_map[tuple(antinode_loc)] = True
            antinode_loc += direction

answer = antinode_map.sum()
print("Part Two:", answer)
