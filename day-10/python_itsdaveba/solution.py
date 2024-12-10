import numpy as np

with open("test.txt") as file:
    input = file.read()

topographic_map = np.array(list(map(list, input.splitlines())), dtype=int)
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right

START_HEIGHT = 0
END_HEIGHT = 9


# find all the trail end locations with DFS
def trail_ends(location, height):
    if height == END_HEIGHT:
        return [tuple(location)]

    ends = []
    next_locations = location + directions

    # check out-of-bounds
    in_bounds = np.all((next_locations >= 0) & (next_locations < topographic_map.shape), axis=1)

    next_locations = next_locations[in_bounds]
    next_heights = topographic_map[next_locations[:, 0], next_locations[:, 1]]

    # check height increases by exactly 1
    uphill = next_heights == height + 1

    for next_location in next_locations[uphill]:
        ends.extend(trail_ends(next_location, height + 1))

    return ends


scores = ratings = 0
trailheads = np.argwhere(topographic_map == START_HEIGHT)

for trailhead_location in trailheads:
    ends = trail_ends(trailhead_location, START_HEIGHT)
    scores += len(set(ends))
    ratings += len(ends)

print("Part One:", scores)
print("Part Two:", ratings)
