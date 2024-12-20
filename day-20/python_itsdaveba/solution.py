import numpy as np
from collections import Counter

with open("input.txt") as file:
    input = file.read()

racetrack_map = np.array(list(map(list, input.splitlines())))
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right

TRACK = "."
START = "S"
END = "E"
WALL = "#"


node = start = tuple(np.argwhere(racetrack_map == START)[0])
distance = np.full_like(racetrack_map, np.inf, dtype=float)

# find path and update distance
prev = {}
distance[start] = 0
while racetrack_map[node] != END:
    next_nodes = np.add(node, directions)

    # check walls
    no_collision = racetrack_map[next_nodes[:, 0], next_nodes[:, 1]] != "#"
    next_nodes = next_nodes[no_collision]

    # check not visited
    not_visited = distance[next_nodes[:, 0], next_nodes[:, 1]] == np.inf
    next_node = tuple(next_nodes[not_visited][0])

    # update distance, prev, and stack
    distance[next_node] = distance[node] + 1
    prev[next_node] = node
    node = next_node


# total number of cheats, grouped by the amount of time they save
def get_num_cheats(end_node, prev, cheat_length):
    num_cheats = Counter()

    node = end_node
    while node in prev.keys():
        for dist in range(1, cheat_length + 1):
            # list of all nodes at dist
            prev_nodes = list(map(tuple, np.add(node, [(-dist, 0), (dist, 0)])))
            for vertical in range(-dist + 1, dist):
                horizontal = dist - abs(vertical)
                prev_nodes.extend(map(tuple, np.add(node, [(vertical, -horizontal), (vertical, horizontal)])))
            prev_nodes = np.array(prev_nodes)

            # check out-of-bounds
            in_bounds = np.all((0 <= prev_nodes) & (prev_nodes < racetrack_map.shape), axis=1)
            prev_nodes = prev_nodes[in_bounds]

            # check walls
            no_collision = racetrack_map[prev_nodes[:, 0], prev_nodes[:, 1]] != "#"
            prev_nodes = prev_nodes[no_collision]

            # check visited through cheat
            difference = distance[node] - distance[prev_nodes[:, 0], prev_nodes[:, 1]]
            difference = difference[difference > dist]

            # update counter
            num_cheats.update(map(int, difference - dist))
        node = prev[node]

    return num_cheats


num_cheats = get_num_cheats(node, prev, 2)
print("Part One:", sum([num_cheats[key] for key in num_cheats if key >= 100]))

num_cheats = get_num_cheats(node, prev, 20)
print("Part Two:", sum([num_cheats[key] for key in num_cheats if key >= 100]))
