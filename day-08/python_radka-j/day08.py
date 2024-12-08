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


antinodes_part1 = []
antinodes_part2 = []

for antenna, positions in antenna_positions.items():
    for pos1, pos2 in itertools.combinations(positions, 2):
        direction = (pos2[0] - pos1[0], pos2[1] - pos1[1])
        an_plus = (pos2[0] + direction[0], pos2[1] + direction[1])
        an_min = (pos1[0] - direction[0], pos1[1] - direction[1])

        # PART 1

        if in_bounds(an_plus):
            antinodes_part1.append(an_plus)
        if in_bounds(an_min):
            antinodes_part1.append(an_min)

        # PART 2

        antinodes_part2.append(pos1)
        antinodes_part2.append(pos2)

        while in_bounds(an_plus):
            antinodes_part2.append(an_plus)
            an_plus = (an_plus[0] + direction[0], an_plus[1] + direction[1])

        while in_bounds(an_min):
            antinodes_part2.append(an_min)
            an_min = (an_min[0] - direction[0], an_min[1] - direction[1])


print("part 1: ", len(set(antinodes_part1)))

print("part 2: ", len(set(antinodes_part2)))
