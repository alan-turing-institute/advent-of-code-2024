import os
import numpy as np


def parse_file(file_path):
    with open(os.path.join(file_path)) as f:
        lines = f.read().splitlines()
    return np.array([[char for char in l] for l in lines])


def move_through_trail(pos, moves):
    j, i = pos

    for move in moves:
        if move == "L":
            i -= 1
        elif move == "R":
            i += 1
        elif move == "U":
            j -= 1
        elif move == "D":
            j += 1

    return (j, i)

def been_here_before(pos, total_positions):
    for i in total_positions:
        if i[0] == pos[0] and i[1] == pos[1]:
            return True
    return False


def valid_move(trail, pos, moves, region_value, total_positions):
    j, i = move_through_trail(pos, moves)
    if trail[j][i] != region_value:
        return False
    if been_here_before([j,i], total_positions):
        return False

    return True


def count_perimeter(data, x, y):
    neighbour_offsets = [(-1, 0), (0, -1), (0, 1), (1, 0)]

    neighbours = []
    count = 0
    for dx, dy in neighbour_offsets:
        nx, ny = x + dx, y + dy
        if data[nx, ny] == value:
            neighbours.append([nx,ny])
            count += 1


    return 4 - count

def find_corners(all_positions, data):
    # Predefined corner patterns (relative offsets)
    top_left = [(-1, -1), (-1, 0), (0, -1)]
    top_right = [(1, -1), (1, 0), (0, -1)]
    bottom_left = [(-1, 1), (-1, 0), (0, 1)]
    bottom_right = [(1, 1), (1, 0), (0, 1)]

    corners = [top_left, top_right, bottom_left, bottom_right]

    n_corners = 0

    for x, y in all_positions:
        center_value = data[x, y]

        for corner_offsets in corners:
            diag_offset = corner_offsets[0]
            others = corner_offsets[1:]

            diag_val = data[x + diag_offset[0], y + diag_offset[1]]
            others_vals = [data[x + dx, y + dy] for dx, dy in others]

            # Conditions for counting a corner:
            if all(val != center_value for val in others_vals):
                n_corners += 1
            elif all(val == center_value for val in others_vals) and diag_val != center_value:
                n_corners += 1

    return n_corners


def compute(region_value, data):
    positions = np.argwhere(data == region_value)

    regions = []
    cost_perimeter = 0
    cost_sides = 0

    for initial_pos in positions:
        stack = []  # Use a stack for DFS
        path = ""
        stack.append(path)

        if been_here_before(initial_pos, regions):
            continue
        all_positions = []
        all_positions.append(initial_pos)

        while stack:
            path = stack.pop()  # Get the last path from the stack

            # Add new paths to the stack
            for next_step in ["L", "R", "U", "D"]:

                # Check if the new path is valid
                if valid_move(data, initial_pos, path + next_step, region_value, all_positions):
                    updated_path = path + next_step
                    stack.append(updated_path)
                    pos0, pos1 = move_through_trail(initial_pos, updated_path)
                    all_positions.append([pos0, pos1])
                    regions.append([pos0, pos1])

        area = len(all_positions)
        per =  sum([count_perimeter(data, i[0], i[1]) for i in all_positions])
        s = find_corners(all_positions,data)

        cost_perimeter += area * per
        cost_sides += area * s

    return cost_perimeter, cost_sides

    print("Cost for region", region_value, "is", cost)


if __name__ == "__main__":

    import time

    time_start1 = time.time()
    file_name = "input.txt"
    #file_name = "test4.txt"

    data = parse_file(file_name)

    data = np.pad(data, 1, mode='constant', constant_values='.')

    values = np.unique(data)

    total_cost_perimeter = 0
    total_cost_side = 0

    for value in values:
        if value == ".":
            continue
        perimeter, side = compute(value, data)
        total_cost_side += side
        total_cost_perimeter += perimeter

    print("Part1: total cost sides", (total_cost_perimeter))
    print("Part2: total cost sides", (total_cost_side))




