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
def shortest_distance(grid, start_pos, end_pos):
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

        # visit and push to queue
        visited[next_coords[:, 0], next_coords[:, 1]] = True
        queue.extend(map(lambda x: (dist + 1, tuple(x)), next_coords))

    if queue:
        return queue[0][0]  # shortest distance
    return -1  # no path


grid = np.full(SHAPE, SAFE, dtype=int)
grid[bytes[:NUM_BYTES][:, 0], bytes[:NUM_BYTES][:, 1]] = CORRUPTED

print("Part One:", shortest_distance(grid, START_POS, END_POS))


# Brute Force (no proud of this :/)
for i in range(NUM_BYTES, len(bytes)):
    grid[tuple(bytes[i])] = CORRUPTED
    if shortest_distance(grid, START_POS, END_POS) < 0:
        break

print("Part Two:", ",".join(map(str, bytes[i])))
