from itertools import product
import numpy as np

with open("input.txt") as file:
    input = file.read()

guard_map = np.array(list(map(list, input.splitlines())))

EMPTY = "."
OBSTACLE = "#"
GUARD_ORIENTATION = ["^", ">", "v", "<"]
VISIED_ORIENTATION = [1, 2, 4, 8]
DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # up, right, down, left


# Part One

# find starting guard position and orientation
start_position = None
start_dir = None
for pos in product(*map(range, guard_map.shape)):
    if guard_map[pos] in GUARD_ORIENTATION:
        start_position = np.array(pos)
        start_dir = GUARD_ORIENTATION.index(guard_map[pos])
        break

# find all visited positions
def find_visited(guard_map, start_position, dir):
    last_position = None
    position = start_position.copy()
    visited = np.zeros_like(guard_map, dtype=int)
    while np.all((position >= 0) & (position < guard_map.shape)):
        if guard_map[tuple(position)] != OBSTACLE:  # check for obstacle in front
            if visited[tuple(position)] & VISIED_ORIENTATION[dir]:  # detect loops for part two
                return None
            visited[tuple(position)] |= VISIED_ORIENTATION[dir]
            last_position = position.copy()
            position += DIRECTIONS[dir]
            continue
        dir = (dir + 1) % 4  # turn right 90 degrees
        position = last_position
    return visited

visited = find_visited(guard_map, start_position, start_dir)
answer = np.where(visited != 0, 1, 0).sum()
print(answer)


# Part Two

# test original visited positions
answer = 0
for pos in zip(*np.where(visited != 0)):
    if np.any(pos != start_position):
        new_map = guard_map.copy()
        new_map[pos] = OBSTACLE
        if find_visited(new_map, start_position, start_dir) is None:  # loop found
            answer += 1

print(answer)
