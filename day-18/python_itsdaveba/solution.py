import numpy as np
from collections import deque

with open("input.txt") as file:
    input = file.read()

SHAPE = (71, 71)
NUM_BYTES = 1024

SAFE = 0
CORRUPTED = 1
START_POS = (0, 0)
END_POS = tuple(s - 1 for s in SHAPE)

bytes = np.array([line.split(",") for line in input.splitlines()], dtype=int)
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right


# Breadth First Search
def shortest_distance(grid, start_pos, end_pos, prev):
    visited = np.zeros_like(grid, dtype=bool)
    visited[start_pos] = True
    queue = deque([(0, start_pos)])  # dist, coord

    while queue and queue[0][1] != end_pos:
        dist, coord = queue.popleft()
        next_coords = np.add(coord, directions)

        # check out-of-bounds
        in_bounds = np.all((0 <= next_coords) & (next_coords < SHAPE), axis=1)
        next_coords = next_coords[in_bounds]

        # check for safe locations
        no_corrupted = grid[next_coords[:, 0], next_coords[:, 1]] != CORRUPTED
        next_coords = next_coords[no_corrupted]

        # check for unvisited locations
        no_visited = ~visited[next_coords[:, 0], next_coords[:, 1]]
        next_coords = next_coords[no_visited]

        # visit, update prev, and push to queue
        visited[next_coords[:, 0], next_coords[:, 1]] = True
        prev.update(dict.fromkeys(map(tuple, next_coords), coord))
        queue.extend(map(lambda nc: (dist + 1, tuple(nc)), next_coords))

    if queue:
        return queue[0][0]  # shortest distance
    return -1  # no path


def get_path(start_pos, end_pos, prev):
    coord = end_pos
    path = [coord]
    while coord != start_pos:
        coord = prev[coord]
        path.append(coord)
    return path[::-1]


prev = {}
grid = np.full(SHAPE, SAFE, dtype=int)
grid[bytes[:NUM_BYTES][:, 0], bytes[:NUM_BYTES][:, 1]] = CORRUPTED  # update grid

print("Part One:", shortest_distance(grid, START_POS, END_POS, prev))


path_set = set(get_path(START_POS, END_POS, prev))

for byte in map(tuple, bytes[NUM_BYTES:]):
    grid[byte] = CORRUPTED  # update grid
    if byte in path_set:  # check if the corrupted byte lies on the optimal path
        if shortest_distance(grid, START_POS, END_POS, prev) < 0:  # no path
            break
        path_set = set(get_path(START_POS, END_POS, prev))  # new optimal path

print("Part Two:", ",".join(map(str, byte)))
