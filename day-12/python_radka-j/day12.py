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
    Given a list of perimeter positions (i.e. locations just outside the plot area),
    count the number of sides that the plot has.
    """
    sides = 0

    # if left plot by moving left/right--> get unique column indexes (idx=1) that reached
    # from this direction and look for continuous row values (idx=0) in each column
    # if left plot by moving top/down --> get unique row indexes (idx=0) that reached
    # from this direction and look for continuos column values (idx=1) in each row
    for direction, border_idx, search_idx in [
        ("right", 1, 0),
        ("left", 1, 0),
        ("up", 0, 1),
        ("down", 0, 1),
    ]:

        to_explore = [pos for pos in perimeter if pos[2] == direction]
        # get the unique row/column indexes
        indexes = list(set([pos[border_idx] for pos in to_explore]))

        # each index is row/wcolumn --> check for continuous column/row values
        for idx in indexes:
            rows = [pos[search_idx] for pos in to_explore if pos[border_idx] == idx]
            # sort and get diff between adjacent values
            rows = np.array(sorted(rows))
            diffs = rows[1:] - rows[:-1]
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
