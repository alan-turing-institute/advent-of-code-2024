import numpy as np

with open("input.txt") as f:
    lines = f.read().splitlines()

grid = np.array([list(l) for l in lines])

# =================================================================
# FUNCTIONS
# =================================================================


def change_direction(direction):
    if direction == (0, 1) or direction == (0, -1):
        return [(1, 0), (-1, 0)]
    else:
        return [(0, 1), (0, -1)]


def next_moves(curr_pos, curr_direction):
    """
    move forward (unless wall in the away) or turn left/right
    also returns score/distance of each move
    """
    moves = []
    scores = []
    new_pos = (curr_pos[0] + curr_direction[0], curr_pos[1] + curr_direction[1])
    if grid[new_pos[0], new_pos[1]] != "#":
        moves.append((new_pos, curr_direction))
        scores.append(curr_score + 1)
    new_direction1, new_direction2 = change_direction(curr_direction)
    moves.extend(
        [
            (curr_pos, new_direction1),
            (curr_pos, new_direction2),
        ]
    )
    scores.extend([curr_score + 1000, curr_score + 1000])
    return moves, scores


def update_neighbours(curr_node, new_node, curr_score, neighbours):
    """
    PART 2: for each node visited, keep track of which node(s)! preceded it in the
    shortest path to that node - note that this can be multiple so we keep a list
    `neighbours` = {<node>: (<shortest distance>, [<all preceding nodes at this distance>])}

    - if haven't seen new_node yet
        - just add it to the neighbours dictionary with curr_node as its best neighour (so far)
    - otherwise
        - if we got to new_node faster (lower score) than ever before, start new list of
            prior neighbours
        - if the score/distance is the same as previously recorded, than just append
            neihbour to existing list
    """
    if new_node not in neighbours:
        neighbours[new_node] = (curr_score, [curr_node])
    else:
        lowest_score = neighbours[new_node][0]
        if curr_score < lowest_score:
            neighbours[new_node] = (curr_score, [curr_node])
        elif curr_score == lowest_score:
            neighbours[new_node][1].append(curr_node)
    return neighbours


# =================================================================
# Djikstra --> build "priority queue":
# - a node is a position and a direction
# - values are distance to each unvisited node from the start node
# - start with infinite distance for all nodes except start
# =================================================================
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

queue[((start_i, start_j), (0, 1))] = 0


# =================================================================
# Find all shortest paths to the end node
# =================================================================
neighbours = {}
lowest_score = np.inf
while queue:

    # get the next node with shortest distance to start pos
    curr_node = min(queue, key=queue.get)
    curr_pos, curr_direction = curr_node
    curr_score = queue[curr_node]

    # if only infinite distance nodes remain in queue - they are unreachable
    if curr_score == np.inf:
        break

    # no point exploring longer paths
    if curr_score > lowest_score:
        break

    # end condition
    if grid[curr_pos[0]][curr_pos[1]] == "E":
        end_node = curr_node
        if curr_score < lowest_score:
            lowest_score = curr_score
        # for part 1 - could end once get here
        # break

    # update distances to neighbours that have not visited yet
    # neighbour = move forward or change direction (right/left)
    moves, scores = next_moves(curr_pos, curr_direction)
    for new_node, new_score in zip(moves, scores):
        if new_node in queue:
            queue[new_node] = min(queue[new_node], new_score)
        neighbours = update_neighbours(curr_node, new_node, new_score, neighbours)

    # remove current node from queue (the univisited set)
    del queue[curr_node]

print("PART 1:", lowest_score)

# get all nodes in all paths that led to the end node (at shortest possible distance travelled)
stack = [end_node]
node_list = set()
while stack:
    curr_node = stack.pop()
    node_list.add(curr_node)
    for node in neighbours[curr_node][1]:
        if node not in node_list:
            stack.append(node)

print("PART 2: ", len(set([pos for pos, direction in node_list])))
