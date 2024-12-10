import numpy as np

with open("input.txt") as f:
    lines = f.read().splitlines()
grid = np.array([[int(n) for n in line] for line in lines])

start_indices = np.where(grid == 0)
start_positions = [(i, j) for i, j in zip(start_indices[0], start_indices[1])]


def valid_moves(pos):
    """
    Return positions of valid moves from `pos` - move up by 1 each step.
    """
    children = []
    i, j = pos
    # up
    if i > 0:
        if grid[i - 1][j] - grid[i][j] == 1:
            children.append((i - 1, j))
    # down
    if i < len(grid) - 1:
        if grid[i + 1][j] - grid[i][j] == 1:
            children.append((i + 1, j))
    # right
    if j < len(grid[0]) - 1:
        if grid[i][j + 1] - grid[i][j] == 1:
            children.append((i, j + 1))
    # left
    if j > 0:
        if grid[i][j - 1] - grid[i][j] == 1:
            children.append((i, j - 1))

    return children


def dfs(start_pos):

    stack = [start_pos]
    # keep track of all 9s that reach (can get there multiple ways so will have duplicates)
    reached = []

    while stack:
        curr_pos = stack.pop()
        if grid[curr_pos[0], curr_pos[1]] == 9:
            reached.append(curr_pos)
        for pos in valid_moves(curr_pos):
            stack.append(pos)

    return reached


tot1 = 0
tot2 = 0
for pos in start_positions:
    paths = dfs(pos)
    # unique destinations reached
    tot1 += len(set(paths))
    # number of paths walked
    tot2 += len(paths)

print("part 1: ", tot1)
print("part 2: ", tot2)
