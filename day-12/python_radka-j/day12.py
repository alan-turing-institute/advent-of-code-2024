import numpy as np

with open("input.txt") as f:
    lines = f.read().splitlines()
grid = [list(line) for line in lines]


def in_bounds(pos):
    if pos[0] < 0 or pos[1] < 0 or pos[0] >= len(grid) or pos[1] >= len(grid[0]):
        return False
    return True


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
            i, j = curr_pos
            adjacents = [
                (i + 1, j, "down"),
                (i - 1, j, "up"),
                (i, j + 1, "right"),
                (i, j - 1, "left"),
            ]
            valid_moves = []
            invalid_moves = []
            for adj_pos in adjacents:
                if (
                    in_bounds(adj_pos)
                    and grid[adj_pos[0]][adj_pos[1]] == grid[curr_pos[0]][curr_pos[1]]
                ):
                    valid_moves.append(adj_pos)
                else:
                    invalid_moves.append(adj_pos)
            perimeter.extend(invalid_moves)
            for i, j, _ in valid_moves:
                pos = (i, j)
                stack.append(pos)
    return area, perimeter


def count_sides(perimeter):
    """
    Given a list of perimeter positions (i.e. locations just outside the plot area),
    count the number of sides that the plot has.
    """
    sides = 0

    # if left plot by moving left/right --> for each position (i,j) reached outside the
    # plot area, get unique column indexes (j) of the positions reached from this
    # direction and count continuous row values (i)
    # if left plot by moving top/down --> get unique row indexes (i) that reached from
    # this direction and count continuous column values (j)
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
            vals = [pos[search_idx] for pos in to_explore if pos[border_idx] == idx]
            # sort and get diff between adjacent values
            vals = np.array(sorted(vals))
            diffs = vals[1:] - vals[:-1]
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
