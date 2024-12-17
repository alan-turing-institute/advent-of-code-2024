import os
from random import random

import numpy as np
import heapq

def parse_file(file_path):
    """Parse the file into a 2D numpy array of characters."""
    with open(file_path) as f:
        lines = f.read().splitlines()
    return np.array([list(line) for line in lines])

def move_position(start_pos, moves):
    """Move through the trail based on a sequence of moves."""
    j, i = start_pos
    path_positions = []

    for move in moves:
        if move == "L":
            i -= 1
        elif move == "R":
            i += 1
        elif move == "U":
            j -= 1
        elif move == "D":
            j += 1
        path_positions.append((j, i))

    return (j, i), path_positions

def move_position_simple(start_pos, moves):
    """Move through the trail and return the final position."""
    j, i = start_pos

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

def calculate_weight(path):
    """Calculate the weight of a path based on its steps."""
    weight = 1
    last_step = path[0]

    for step in path[1:]:
        weight += 1 if step == last_step else 1001
        last_step = step

    return weight

def is_valid_move(trail, start_pos, moves):
    """Check if the moves lead to a valid position on the trail."""
    j, i = move_position_simple(start_pos, moves)

    if i < 0 or j < 0 or i >= trail.shape[1] or j >= trail.shape[0]:
        return False
    if trail[j][i] == "#":
        return False

    return True

def get_priority_moves(last_move):
    """Get a priority list of moves based on the last move."""
    priority_map = {
        "": ["U", "L", "R"],
        "R": ["R", "U", "D"],
        "D": ["D", "R", "L"],
        "U": ["U", "L", "R"],
        "L": ["L", "U", "D"]
    }
    return priority_map.get(last_move, ["U", "L", "R"])

if __name__ == "__main__":
    import time

    file_name = "input.txt"
    trail = parse_file(file_name)
    start_positions = np.argwhere(trail == "S")

    all_paths = []
    shortest_weight = float("inf")

    time_start = time.time()

    for start in ["R","U"]:
        start_positions = np.argwhere(trail == "S")
        start_pos = tuple(start_positions[0])

        print("Start Position:", start)
        priority_queue = []
        initial_path = start
        heapq.heappush(priority_queue, (0, start_pos, initial_path))

        visited_states = {}

        while priority_queue:
            current_weight, current_pos, path = heapq.heappop(priority_queue)

            if (current_pos, path[-1]) in visited_states and visited_states[(current_pos, path[-1])] < current_weight:
                continue
            visited_states[(current_pos, path[-1])]= current_weight

            j, i = current_pos
            if trail[j][i] == "E":
                shortest_weight = min(shortest_weight, current_weight)
                all_paths.append(path)
                time_start = time.time()


            priority_moves = get_priority_moves(path[-1:])

            for move in priority_moves:
                new_path = path + move
                new_weight = calculate_weight(new_path)

                if new_weight > shortest_weight:
                    continue

                new_pos = move_position_simple(start_pos, new_path)
                if is_valid_move(trail, start_pos, new_path):
                    heapq.heappush(priority_queue, (new_weight, new_pos, new_path))

    print("Part1: Shortest Weight:", shortest_weight+1000)

    all_positions = []
    for path in np.unique(all_paths):
        _, path_positions = move_position(tuple(start_positions[0]), path)
        all_positions.extend(path_positions)

    print("Part2: Unique Positions Visited:", len(set(all_positions))+1)
    print("Execution Time:", time.time() - time_start)

