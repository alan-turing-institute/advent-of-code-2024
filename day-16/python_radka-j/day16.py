import numpy as np

with open("input.txt") as f:
    lines = f.read().splitlines()

grid = np.array([list(l) for l in lines])


def change_direction(direction):
    if direction == (0, 1) or direction == (0, -1):
        return [(1, 0), (-1, 0)]
    else:
        return [(0, 1), (0, -1)]


# Djikstra
# build "priority queue":
# - a node is a position and a direction
# - values are distance to each unvisited node from the start node
# - start with infinite distance for all nodes
queue = {}

directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]
for i, line in enumerate(grid):
    for j, char in enumerate(line):
        if char == "E" or char == "." or char == "S":
            for direction in directions:
                node = ((i, j), direction)
                queue[node] = np.inf
            if char == "S":
                start_i = i
                start_j = j

# distance is 0 from start to start
queue[((start_i, start_j), (0, 1))] = 0

while queue:

    # get the node with currently shortest distance to start pos
    curr_node = min(queue, key=queue.get)
    curr_pos, curr_direction = curr_node
    curr_score = queue[curr_node]

    # if only infinite distance nodes remain in queue - they are unreachable
    if curr_score == np.inf:
        break

    # end condition
    if grid[curr_pos[0]][curr_pos[1]] == "E":
        print("PART 1:", curr_score)
        break

    # update distances to neighbours: move forward or change direction
    new_pos = (curr_pos[0] + curr_direction[0], curr_pos[1] + curr_direction[1])
    if (new_pos, curr_direction) in queue:
        if grid[new_pos[0], new_pos[1]] != "#":
            new_node = (new_pos, curr_direction)
            queue[new_node] = min(queue[new_node], curr_score + 1)

    new_direction1, new_direction2 = change_direction(curr_direction)
    if (curr_pos, new_direction1) in queue:
        new_node = (curr_pos, new_direction1)
        queue[new_node] = min(queue[new_node], curr_score + 1000)
    if (curr_pos, new_direction2) in queue:
        node = (curr_pos, new_direction2)
        queue[node] = min(queue[node], curr_score + 1000)

    # remove current node from queue (the univisited set)
    del queue[curr_node]
