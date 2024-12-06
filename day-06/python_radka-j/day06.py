from collections import defaultdict

# ===========================================
# PARSE INPUT
# ===========================================

with open("input.txt") as f:
    lines = f.read().splitlines()

grid = [list(l) for l in lines]

for i, line in enumerate(grid):
    for j, pos in enumerate(line):
        if pos == "^":
            start_pos = (i, j)

# ===========================================
# HELPER FUNCTIONS
# ===========================================


def turn_right(direction):
    # left -> up
    if direction == [0, -1]:
        return [-1, 0]
    # up -> right
    elif direction == [-1, 0]:
        return [0, 1]
    # right -> down
    elif direction == [0, 1]:
        return [1, 0]
    # down -> left
    elif direction == [1, 0]:
        return [0, -1]


def left_grid(pos):
    if pos[0] < 0 or pos[1] < 0 or pos[0] >= len(grid) or pos[1] >= len(grid[0]):
        return True
    return False


def walk(grid):
    curr_pos = start_pos
    visited = [curr_pos]

    # both test and real input start with going up
    # track past directions at each pos to check for loops
    direction = [-1, 0]
    directions = defaultdict(list)
    directions[curr_pos] = [direction]

    left = False
    loop = False

    while not left or not loop:

        new_pos = (curr_pos[0] + direction[0], curr_pos[1] + direction[1])

        # have we left yet?
        if left_grid(new_pos):
            left = True
            break

        # are we back at some position going in direction we've gone before?
        elif new_pos in visited and direction in directions[new_pos]:
            loop = True
            break

        # do we need to turn?
        elif grid[new_pos[0]][new_pos[1]] == "#":
            direction = turn_right(direction)
            directions[curr_pos].append(direction)

        else:
            visited.append(new_pos)
            curr_pos = new_pos
            directions[curr_pos].append(direction)

    return visited, loop


# ===========================================
# PART 1
# ===========================================
visited, _ = walk(grid)
unique_visited = set(visited)

print("part 1: ", len(unique_visited))

# ===========================================
# PART 2
# - put obstacles in the guard's original path
# - Q: is there a way to eliminate some options?
# ===========================================

count = 0
for pos in unique_visited:
    i, j = pos
    if grid[i][j] != "^":
        # print("updated: ", i, j)
        updated_grid = [list(l) for l in lines]
        updated_grid[i][j] = "#"
        _, has_loop = walk(updated_grid)
        if has_loop:
            count += 1

print("part 2: ", count)
