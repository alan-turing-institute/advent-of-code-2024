from collections import Counter, defaultdict

with open("input.txt") as f:
    lines = f.read().splitlines()


# ====================================================
# get positions and counts of robots at each time step
# ====================================================

width = 101
height = 103
max_t = width * height

positions = {t: defaultdict(int) for t in range(max_t)}
for line in lines:
    p, v = line.split(" ")
    x, y = [int(val) for val in p.split("=")[1].split(",")]
    dx, dy = [int(val) for val in v.split("=")[1].split(",")]
    for t in range(max_t):
        # use modulo to wrap around
        x = (x + dx) % width
        y = (y + dy) % height
        positions[t][(x, y)] += 1


# =====================================
# PART 1
# =====================================


def quadrant_counts(
    positions_dict, width_split=(width - 1) / 2, height_split=(height - 1) / 2
):
    q1_count = 0
    q2_count = 0
    q3_count = 0
    q4_count = 0

    for pos, count in positions_dict.items():
        # top left corner
        if pos[0] < width_split and pos[1] < height_split:
            q1_count += count
        # top right corner
        elif pos[0] > width_split and pos[1] < height_split:
            q2_count += count
        # bottom left corner
        elif pos[0] < width_split and pos[1] > height_split:
            q3_count += count
        # bottom right corner
        elif pos[0] > width_split and pos[1] > height_split:
            q4_count += count
    return [q1_count, q2_count, q3_count, q4_count]


tot = 1
quad_counts = quadrant_counts(positions[99])
for count in quad_counts:
    tot *= count
print("part 1: ", tot)


# =====================================
# PART 2
# count time at which have most robots in unique positions around what should be the tree trunk
# =====================================

middle_col = (width - 1) / 2

max_unique_pos_count = 0
best_t = max_t
for t in range(max_t):
    unique_pos_count = 0
    for i in range(-2, 2):
        occupied_col_positions = [
            pos for pos in positions[t].keys() if pos[1] == middle_col + i
        ]
        unique_pos_count += len(occupied_col_positions)
    if unique_pos_count > max_unique_pos_count:
        max_unique_pos_count = unique_pos_count
        best_t = t

print("part 2: ", best_t + 1)
