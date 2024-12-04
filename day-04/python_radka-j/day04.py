with open("input.txt") as f:
    lines = f.read().splitlines()

grid = [list(l) for l in lines]


# ===========================================
# HELPER FUNCTIONS
#
# all return the originally position if we can't move in a given direction
# since it won't have a new letter and so search won't continue
# ===========================================


def go_up(i, j):
    if i > 0:
        return [i - 1, j]
    return [i, j]


def go_down(i, j):
    if i < len(grid) - 1:
        return [i + 1, j]
    return [i, j]


def go_right(i, j):
    if j < len(grid[0]) - 1:
        return [i, j + 1]
    return [i, j]


def go_left(i, j):
    if j > 0:
        return [i, j - 1]
    return [i, j]


def go_right_up(i, j):
    if i > 0 and j < len(grid[0]) - 1:
        return [i - 1, j + 1]
    return [i, j]


def go_left_up(i, j):
    if i > 0 and j > 0:
        return [i - 1, j - 1]
    return [i, j]


def go_right_down(i, j):
    if i < len(grid) - 1 and j < len(grid[0]) - 1:
        return [i + 1, j + 1]
    return [i, j]


def go_left_down(i, j):
    if i < len(grid) - 1 and j > 0:
        return [i + 1, j - 1]
    return [i, j]


# ===========================================
# PART 1
# ===========================================


def count_xmas(i, j):
    """
    Check all directions from [i, j] pos on whether they form "XMAS" and return count.
    """
    found = 0
    if grid[i][j] == "X":
        for direction in [
            go_up,
            go_down,
            go_right,
            go_left,
            go_right_up,
            go_right_down,
            go_left_up,
            go_left_down,
        ]:
            i_next, j_next = direction(i, j)
            if grid[i_next][j_next] == "M":
                i_next, j_next = direction(i_next, j_next)
                if grid[i_next][j_next] == "A":
                    i_next, j_next = direction(i_next, j_next)
                    if grid[i_next][j_next] == "S":
                        found += 1
    return found


tot = 0
for i, line in enumerate(grid):
    for j, pos in enumerate(line):
        tot += count_xmas(i, j)

print("Part 1: ", tot)


# ===========================================
# PART 2
# ===========================================


def check_mas(i, j):
    """
    Check if there is a MAS in an x-shape
    """
    found = False
    if grid[i][j] == "A":
        # get the diagonal letters
        i_, j_ = go_right_up(i, j)
        ru = grid[i_][j_]
        i_, j_ = go_left_up(i, j)
        lu = grid[i_][j_]
        i_, j_ = go_right_down(i, j)
        rd = grid[i_][j_]
        i_, j_ = go_left_down(i, j)
        ld = grid[i_][j_]

        if ru == "M" and ld == "S" and lu == "M" and rd == "S":
            found = True
        elif ru == "S" and ld == "M" and lu == "S" and rd == "M":
            found = True
        elif ru == "M" and ld == "S" and lu == "S" and rd == "M":
            found = True
        elif ru == "S" and ld == "M" and lu == "M" and rd == "S":
            found = True

    return found


tot = 0
for i, line in enumerate(grid):
    for j, pos in enumerate(line):
        if check_mas(i, j):
            tot += 1

print("part 2: ", tot)
