import numpy as np

with open("warehouse.txt") as f:
    warehouse = f.read().splitlines()

with open("moves.txt") as f:
    moves_list = f.read().splitlines()

# ===========================================
# PART 1
# ===========================================


def update_grid(direction):
    """
    update grid by 1 step in direction if the robot can move that way
    - move all adjacent boxes as well
    """

    if direction == "<":
        di = 0
        dj = -1
    elif direction == ">":
        di = 0
        dj = 1
    elif direction == "^":
        di = -1
        dj = 0
    elif direction == "v":
        di = 1
        dj = 0

    robot_row, robot_col = np.argwhere(grid == "@")[0]
    # see if can move
    i, j = (robot_row + di, robot_col + dj)
    can_move = False
    while grid[i, j] != "#":
        if grid[i, j] == ".":
            can_move = True
            break
        i += di
        j += dj

    # move adjacent boxes and robot by 1
    if can_move:
        i, j = (robot_row + di, robot_col + dj)
        while grid[i, j] == "O":
            i += di
            j += dj
        # if there are no boxes to move, this gets overwritten below by moving
        # the robot to this pos
        grid[i, j] = "O"
        grid[robot_row, robot_col] = "."
        grid[robot_row + di, robot_col + dj] = "@"

    return grid


grid = np.array([list(line) for line in warehouse])
for move_line in moves_list:
    for move in move_line:
        grid = update_grid(move)

tot = 0
for box in np.argwhere(grid == "O"):
    tot += 100 * box[0] + box[1]
print("part 1: ", tot)

# ===========================================
# PART 2
# ===========================================

# 1. double grid width
larger_warehouse = []
for line in warehouse:
    new_line = []
    for char in line:
        if char == "#":
            new_line.extend(["#", "#"])
        elif char == "O":
            new_line.extend(["[", "]"])
        elif char == ".":
            new_line.extend([".", "."])
        elif char == "@":
            new_line.extend(["@", "."])
    # print("".join(new_line))
    larger_warehouse.append(new_line)


# 2. move robot and boxes around
grid = np.array(larger_warehouse)
