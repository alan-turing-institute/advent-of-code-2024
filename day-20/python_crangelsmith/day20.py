import os
from random import random

import numpy as np
import heapq


import numpy as np
import heapq

def parse_file(file_path):
    """Parse the file into a 2D numpy array of characters."""
    with open(file_path) as f:
        lines = f.read().splitlines()
    return np.array([list(line) for line in lines])


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


def calculate_weight(start, end):
    """Calculate the weight of a path based on its steps."""
    manhattan = abs(start[0] - end[0]) + abs(start[1] - end[1])

    return manhattan


def is_valid_move(trail, position):
    """Check if the moves lead to a valid position on the trail."""
    y, x = position

    if x < 0 or y < 0 or x >= trail.shape[1] or y >= trail.shape[0]:
        return False
    if trail[y][x] == "#":
        return False

    return True


def simulate(matrix,start_pos, target_pos):

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
            new_pos, _ = move_position(current_pos, move)
            new_weight = calculate_weight(new_pos, target_pos)

            if is_valid_move(matrix, new_pos):
                heapq.heappush(priority_queue, (new_weight, new_pos, new_path))

    _, final_positions = move_position(start_pos, final_path)

    return final_positions


if __name__ == "__main__":
    import time

    file_name = "input.txt"
    #file_name = "test.txt"

    matrix = parse_file(file_name)

    start_pos = tuple(np.argwhere(matrix == "S")[0])
    target_pos = tuple(np.argwhere(matrix == "E")[0])

    hashes = tuple(np.argwhere(matrix == "#"))

    hashes = [
        h for h in hashes
        if not (h[0] in {0, len(matrix) - 1} or h[1] in {0, len(matrix[0]) - 1})
    ]

    max_path = len(simulate(matrix,start_pos, target_pos))


    saves = {}
    cheats = 0
    count = 0
    for h in hashes:
        print(count, 'out of', len(hashes))
        matrix[h[0],h[1]] = "."


        visited_states = simulate(matrix,start_pos, target_pos)
        saved_path = max_path - len(visited_states)

        if saved_path> 99:
            cheats += 1

        if saved_path not in saves:
            saves[saved_path] = 1
        else:
            saves[saved_path] += 1

        matrix[h[0], h[1]]  = "#"
        count += 1

    print(saves)
    print(cheats)

