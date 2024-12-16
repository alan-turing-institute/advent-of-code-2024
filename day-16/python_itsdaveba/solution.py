import heapq
import numpy as np
from collections import defaultdict

with open("input.txt") as file:
    input = file.read()

direction = [(0, 1), (-1, 0), (0, -1), (1, 0)]  # east, north, west, south
WALL = "#"
END_TILE = "E"
START_TILE = "S"
INIT_ORIENTATION = 0  # east
FORWARD_SCORE = 1
ROTATE_SCORE = 1000

maze = np.array(list(map(list, input.splitlines())))
start = tuple(np.argwhere(maze == START_TILE)[0])

distance_shape = maze.shape + (4,)  # maze shape + num orientations
distance = np.full(distance_shape, np.inf, dtype=float)  # min distance from start to (tile, orientation)
prev = defaultdict(list)  # (tile, orientation): list of previous (tile, orientation) nodes

distance[start][INIT_ORIENTATION] = 0
pq = [(0, start, INIT_ORIENTATION, None)]  # score, tile, orientation, last_move
while pq:
    score, tile, orientation, last_move = heapq.heappop(pq)
    if maze[tile] == END_TILE:
        break

    # forward
    next_tile = tuple(np.add(tile, direction[orientation]))
    if maze[next_tile] != WALL:
        next_score = score + FORWARD_SCORE
        if next_score <= distance[next_tile][orientation]:
            distance[next_tile][orientation] = next_score
            prev[(next_tile, orientation)].append((tile, orientation))
            heapq.heappush(pq, (next_score, next_tile, orientation, "forward"))

    # rotation
    if last_move != "rotation":
        next_score = score + ROTATE_SCORE
        for next_orientation in [(orientation + 1) % 4, (orientation - 1) % 4]:
            if next_score <= distance[tile][next_orientation]:
                distance[tile][next_orientation] = next_score
                prev[(tile, next_orientation)].append((tile, orientation))
                heapq.heappush(pq, (next_score, tile, next_orientation, "rotation"))


print("Part One:", score)

stack = [(tile, orientation)]
path_tiles = set()
while stack:
    tile, orientation = stack.pop()
    path_tiles.add(tile)
    stack.extend(prev.pop((tile, orientation), []))

print("Part Two:", len(path_tiles))
