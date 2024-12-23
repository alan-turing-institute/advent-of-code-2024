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
    path_positions = [(y,x)]

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


def simulate(matrix, start_pos, target_pos):
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
    # file_name = "test.txt"

    matrix = parse_file(file_name)

    start_pos = tuple(np.argwhere(matrix == "S")[0])
    target_pos = tuple(np.argwhere(matrix == "E")[0])

    path = simulate(matrix, start_pos, target_pos)
    pos_map = {p: i for i, p in enumerate(path)}

    non_hash = list(np.argwhere(matrix != '#'))

    pairs_2 = set()
    discriminator = 100
    for _ in range(len(non_hash)):
        start = non_hash.pop(0)
        for end in non_hash:
            if matrix[end[0], end[1]] != '#':
                manhattan = calculate_weight(start, end)
                if manhattan < 21:
                    n1 = pos_map[tuple(start)]
                    n2 = pos_map[tuple(end)]
                    score = abs(n1 - n2) - manhattan
                    if score >= discriminator:
                        pairs_2.add((tuple(start), tuple(end), score))

    print("Part 2:", len(pairs_2))
