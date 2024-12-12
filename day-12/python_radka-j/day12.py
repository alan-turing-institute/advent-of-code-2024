import numpy as np

with open("input.txt") as f:
    lines = f.read().splitlines()
grid = [list(line) for line in lines]


def valid_moves(pos):
    """
    Move is valid if it is on the grid and has the same plant as `pos`.
    """
    valid = []
    invalid = []
    i, j = pos
    plant = grid[i][j]

    # up
    if i > 0:
        if grid[i - 1][j] == plant:
            valid.append((i - 1, j, "up"))
        else:
            invalid.append((i - 1, j, "up"))
    else:
        invalid.append((i - 1, j, "up"))
    # down
    if i < len(grid) - 1:
        if grid[i + 1][j] == plant:
            valid.append((i + 1, j, "down"))
        else:
            invalid.append((i + 1, j, "down"))
    else:
        invalid.append((i + 1, j, "down"))
    # right
    if j < len(grid[0]) - 1:
        if grid[i][j + 1] == plant:
            valid.append((i, j + 1, "right"))
        else:
            invalid.append((i, j + 1, "right"))
    else:
        invalid.append((i, j + 1, "right"))
    # left
    if j > 0:
        if grid[i][j - 1] == plant:
            valid.append((i, j - 1, "left"))
        else:
            invalid.append((i, j - 1, "left"))
    else:
        invalid.append((i, j - 1, "left"))

    return valid, invalid


def explore_plot(start_pos):
    """
    Given a position, get the area and perimeter of the garden plot.
    """
    # check all adjacent positions
    # if same symbol => increment area
    # if not => add to perimeter
    stack = [start_pos]
    area = 0
    perimeter = []
    while stack:
        curr_pos = stack.pop()
        if curr_pos not in visited:
            area += 1
            visited.append(curr_pos)
            # "borders" are positions just outside the plot
            moves, borders = valid_moves(curr_pos)
            perimeter.extend(borders)
            for i, j, _ in moves:
                pos = (i, j)
                stack.append(pos)
    return area, perimeter


def count_sides(perimeter):
    """
    Given a list of perimeter positions (i.e. locations just outside the plot are),
    count the number of sides that the plot has.
    """
    sides = 0

    # side walls --> got there by horizontal step
    # check for continuities moving up/down
    for direction in ["right", "left"]:

        verticals = [pos for pos in perimeter if pos[2] == direction]
        # get the unique column indexes
        j_idx = list(set([pos[1] for pos in verticals]))

        # each index is a column --> check continuous row values in each given column
        for idx in j_idx:
            rows = [pos[0] for pos in verticals if pos[1] == idx]
            # sort and get diff between adjacent values
            rows = np.array(sorted(rows))
            diffs = rows[1:] - rows[:-1]
            # count discontinuities (+ 1)
            sides += sum(diffs != 1) + 1

    # top/bottom walls --> got there by a vertical step
    # check for continutities moving left/right
    for direction in ["up", "down"]:
        horizontals = [pos for pos in perimeter if pos[2] == direction]
        # get the unique row indexes
        i_idx = list(set([pos[0] for pos in horizontals]))

        # each index is a row --> check continuous column values in each given row
        for idx in i_idx:
            cols = [pos[1] for pos in horizontals if pos[0] == idx]
            # sort and get diff between adjacent values
            cols = np.array(sorted(cols))
            diffs = cols[1:] - cols[:-1]
            # count discontinuities (+ 1)
            sides += sum(diffs != 1) + 1
    return sides


# keep track of visited positions (updated in `explore_plot`)
visited = []
price1 = 0
price2 = 0
for i in range(len(grid)):
    for j in range(len(grid[0])):
        if (i, j) not in visited:
            area_count, perimeter_pos = explore_plot((i, j))
            price1 += area_count * len(perimeter_pos)
            sides = count_sides(perimeter_pos)
            price2 += area_count * sides

print("part 1: ", price1)
print("part 2: ", price2)
