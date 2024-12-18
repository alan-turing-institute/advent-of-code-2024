import os
from random import random

import numpy as np
import heapq


def parse_file(file_path):
    """Parse the file into a 2D numpy array of characters."""
    with open(file_path) as f:
        lines = f.read().splitlines()
    return [list(map(int, line.split(','))) for line in lines]


def move_position(start_pos, moves):
    """Move through the trail based on a sequence of moves."""
    y, x = start_pos
    path_positions = []

    for move in moves:
        if move == "L":
            x -= 1
        elif move == "R":
            x += 1
        elif move == "U":
            y -= 1
        elif move == "D":
            y += 1
        path_positions.append((y, x))

    return (y, x), path_positions


def calculate_weight(path):
    """Calculate the weight of a path based on its steps."""
    return len(path)


def is_valid_move(trail, position):
    """Check if the moves lead to a valid position on the trail."""
    y, x = position

    if x < 0 or y < 0 or x >= trail.shape[1] or y >= trail.shape[0]:
        return False
    if trail[y][x] == "#":
        return False

    return True


def simulate(matrix):
    target_pos = (len(matrix[0]) - 1, len(matrix[0]) - 1)
    start_pos = (0, 0)

    priority_queue = []
    initial_path = ""
    heapq.heappush(priority_queue, (0, start_pos, initial_path))

    visited_states = {}
    final_path = initial_path
    while priority_queue:
        current_weight, current_pos, path = heapq.heappop(priority_queue)

        if len(path) > 0:
            if (current_pos, path[-1]) in visited_states and visited_states[
                (current_pos, path[-1])] <= current_weight:
                continue
            visited_states[(current_pos, path[-1])] = current_weight

        if current_pos == target_pos:
            final_path = path
            break

        for move in ["U", "D", "L", "R"]:
            new_path = path + move
            new_weight = calculate_weight(new_path)

            new_pos, _ = move_position(current_pos, move)
            if is_valid_move(matrix, new_pos):
                heapq.heappush(priority_queue, (new_weight, new_pos, new_path))

    _, final_positions = move_position((0, 0), final_path)

    return final_positions


if __name__ == "__main__":
    import time

    file_name = "input.txt"
    coordinates = parse_file(file_name)

    matrix = np.full((71, 71), ".", dtype=str)

    for i in coordinates[:1024]:
        X = i[0]
        Y = i[1]

        matrix[Y, X] = "#"

    visited_states = simulate(matrix)
    print("Part 1:", len(visited_states))

    ## Part 2
    ## if the new coordinate is not in the visited states, skip it
    n_iterations = 0
    time_start = time.time()
    for new_X, new_Y in coordinates[1024:]:

        matrix[new_Y, new_X] = "#"

        if (new_Y, new_X) not in visited_states:
            continue

        n_iterations += 1
        visited_states = simulate(matrix)

        if len(visited_states) == 0:
            print("Part 2:", new_X, new_Y)
            break

    print("Iterations:", n_iterations)
    print("Time:", time.time() - time_start)
