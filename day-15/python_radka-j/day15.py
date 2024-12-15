import numpy as np

with open("warehouse.txt") as f:
    warehouse = f.read().splitlines()

with open("moves.txt") as f:
    moves_list = f.read().splitlines()

# ===========================================
# PART 1
# ===========================================


def get_direction(symbol):
    if symbol == "<":
        di = 0
        dj = -1
    elif symbol == ">":
        di = 0
        dj = 1
    elif symbol == "^":
        di = -1
        dj = 0
    elif symbol == "v":
        di = 1
        dj = 0
    return (di, dj)


def update_grid_part1(direction):
    """
    update grid by 1 step in the given direction if the robot can move that way
    - move all adjacent boxes as well
    """

    di, dj = get_direction(direction)

    robot_row, robot_col = np.argwhere(grid == "@")[0]
    # see if robot can move in this direction
    i, j = (robot_row + di, robot_col + dj)
    can_move = False
    while grid[i, j] != "#":
        if grid[i, j] == ".":
            can_move = True
            break
        i += di
        j += dj

    # move adjacent boxes and robot
    if can_move:
        i, j = (robot_row + di, robot_col + dj)
        while grid[i, j] == "O":
            i += di
            j += dj
        # note: if there are no boxes to move, the next line gets overwritten
        # by moving the robot to this pos
        grid[i, j] = "O"
        grid[robot_row, robot_col] = "."
        grid[robot_row + di, robot_col + dj] = "@"

    return grid


grid = np.array([list(line) for line in warehouse])
for move_line in moves_list:
    for move in move_line:
        grid = update_grid_part1(move)

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

grid = np.array(larger_warehouse)


# 2. move robot and boxes around
def get_all_boxes(pos, di, grid):
    """
    retrieve all boxes above/below robot `pos` on `grid` (direction indicated by `di`)
    also indicates whether the robot can move in this direction
    """
    # `di` indicates whether moving up or down
    boxes = []
    stack = [pos]
    can_move = True
    while stack:
        curr_pos = stack.pop()
        i, j = curr_pos
        if grid[i, j] == "[":
            boxes.append((i, j))
            boxes.append((i, j + 1))
            # explore positions above the box
            stack.append((i + di, j))
            stack.append((i + di, j + 1))
        elif grid[i, j] == "]":
            boxes.append((i, j))
            boxes.append((i, j - 1))
            # explore positions above this
            stack.append((i + di, j))
            stack.append((i + di, j - 1))
        elif grid[i, j] == "#":
            can_move = False

    return set(boxes), can_move


def update_grid_part2(direction):
    """
    update grid by 1 step in the given direction if the robot can move that way
    - move all adjacent boxes as well
    """

    robot_row, robot_col = np.argwhere(grid == "@")[0]
    di, dj = get_direction(direction)

    # if there is no box in the way - just go ahead
    if grid[robot_row + di, robot_col + dj] == ".":
        grid[robot_row + di, robot_col + dj] = "@"
        grid[robot_row, robot_col] = "."

    # sideways movement is similar to before
    elif direction in [">", "<"]:
        i, j = (robot_row + di, robot_col + dj)
        can_move = False
        while grid[i, j] != "#":
            if grid[i, j] == ".":
                can_move = True
                break
            i += di
            j += dj

        if can_move:
            # move boxes
            j = robot_col + dj
            while grid[i, j] in ["[", "]"]:
                j += dj
            if direction == ">":
                start_pos, end_pos = (robot_col + 2, j + 1)
            else:
                start_pos, end_pos = (j, robot_col)
            symb = "["
            for col in range(start_pos, end_pos):
                grid[robot_row, col] = symb
                if symb == "[":
                    symb = "]"
                else:
                    symb = "["

            # move robot
            grid[robot_row, robot_col] = "."
            grid[robot_row + di, robot_col + dj] = "@"

    # finaly, moving boxes up/down...
    elif direction in ["^", "v"]:
        i, j = (robot_row + di, robot_col + dj)
        # if can_move robot, returns all boxes that need moving
        boxes, can_move = get_all_boxes((i, j), di, grid)
        if direction == "^":
            boxes = sorted(boxes)
        else:
            boxes = sorted(boxes, reverse=True)
        if can_move:
            # the boxes are sorted in ascending/descending row order (depending on
            # direction) so shouldn't need to worry about overwriting
            for i, j in boxes:
                # move box up
                grid[i + di, j] = grid[i, j]
                # replace pos with whatever was the character below it
                grid[i, j] = "."

            # move robot
            grid[robot_row, robot_col] = "."
            grid[robot_row + di, robot_col + dj] = "@"
    return grid


for move_line in moves_list:
    for move in move_line:
        grid = update_grid_part2(move)
        # for line in grid:
        #     print("".join(line))

# 3. compute distance
tot = 0
for box in np.argwhere(grid == "["):
    tot += 100 * box[0] + box[1]
print("part 2: ", tot)
