import itertools
from collections import defaultdict

with open("input.txt") as f:
    lines = f.read().splitlines()

antenna_positions = defaultdict(list)

for i, line in enumerate(lines):
    for j, symbol in enumerate(line):
        if symbol != ".":
            antenna_positions[symbol].append((i, j))


def in_bounds(pos):
    if pos[0] < 0 or pos[1] < 0 or pos[0] >= len(lines) or pos[1] >= len(lines[0]):
        return False
    return True


antinodes1 = []
antinodes2 = []

for antenna, positions in antenna_positions.items():
    for pos1, pos2 in itertools.combinations(positions, 2):
        direction = (pos2[0] - pos1[0], pos2[1] - pos1[1])
        antinode1 = (pos2[0] + direction[0], pos2[1] + direction[1])
        antinode2 = (pos1[0] - direction[0], pos1[1] - direction[1])

        if in_bounds(antinode1):
            antinodes1.append(antinode1)
        if in_bounds(antinode2):
            antinodes1.append(antinode2)

        antinodes2.append(pos1)
        antinodes2.append(pos2)

        while in_bounds(antinode1):
            antinodes2.append(antinode1)
            antinode1 = (antinode1[0] + direction[0], antinode1[1] + direction[1])

        while in_bounds(antinode2):
            antinodes2.append(antinode2)
            antinode2 = (antinode2[0] - direction[0], antinode2[1] - direction[1])


print("part 1: ", len(set(antinodes1)))

print("part 2: ", len(set(antinodes2)))
