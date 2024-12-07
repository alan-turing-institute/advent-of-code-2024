import sys

import numpy as np


def visualise_grid(guard_position, direction, grid):
    if (direction == np.array([-1, 0])).all():
        direction_char = '^'

    elif (direction == np.array([0, 1])).all():
        direction_char = '>'

    elif (direction == np.array([0, -1])).all():
        direction_char = '<'

    elif (direction == np.array([1, 0])).all():
        direction_char = 'v'

    output_grid = grid.copy()
    output_grid[guard_position[0], guard_position[1]] = direction_char

    print(output_grid)
    print()


def part1(contents):
    grid = np.array([[char for char in line] for line in contents.split('\n') if line])
    directions_map = {'^': np.array([-1, 0]),
                      '>': np.array([0, 1]),
                      '<': np.array([0, -1]),
                      'v': np.array([1, 0])}

    rotation = np.array([[0, 1],
                         [-1, 0]])

    for row_coord in range(grid.shape[0]):
        for col_coord in range(grid.shape[1]):
            if grid[row_coord, col_coord] in ('^', '>', '<', 'v'):
                guard_position = np.array([row_coord, col_coord])
                direction = directions_map[grid[row_coord, col_coord]]
                grid[row_coord, col_coord] = '.'

    unique_squares = {(guard_position[0], guard_position[1])}

    while True:
        # visualise_grid(guard_position, direction, grid)
        potential_next_pos = guard_position + direction

        if (potential_next_pos[0] >= grid.shape[0]
                or potential_next_pos[0] < 0
                or potential_next_pos[1] >= grid.shape[1]
                or potential_next_pos[1] < 0):
            break

        elif grid[potential_next_pos[0], potential_next_pos[1]] == '#':
            direction = rotation @ direction

        else:
            guard_position = potential_next_pos
            unique_squares.add((guard_position[0], guard_position[1]))

    return len(unique_squares)


def check_stuck(path):
    if len(path) <= 3:
        return False

    last_two_steps = path[-2:]

    for i in range(len(path) - 3):
        if last_two_steps == path[i: i + 2]:
            return True

    return False


def part2(contents):
    grid = np.array([[char for char in line] for line in contents.split('\n') if line])
    directions_map = {'^': np.array([-1, 0]),
                      '>': np.array([0, 1]),
                      '<': np.array([0, -1]),
                      'v': np.array([1, 0])}

    rotation = np.array([[0, 1],
                         [-1, 0]])

    for row_coord in range(grid.shape[0]):
        for col_coord in range(grid.shape[1]):

            if grid[row_coord, col_coord] in ('^', '>', '<', 'v'):
                start_guard_position = np.array([row_coord, col_coord])
                start_direction = directions_map[grid[row_coord, col_coord]]

                grid[row_coord, col_coord] = '.'

    unique_squares = set([])

    guard_position = start_guard_position.copy()
    direction = start_direction.copy()

    while True:
        # visualise_grid(guard_position, direction, grid)
        potential_next_pos = guard_position + direction

        if (potential_next_pos[0] >= grid.shape[0]
                or potential_next_pos[0] < 0
                or potential_next_pos[1] >= grid.shape[1]
                or potential_next_pos[1] < 0):
            break

        elif grid[potential_next_pos[0], potential_next_pos[1]] == '#':
            direction = rotation @ direction

        else:
            guard_position = potential_next_pos
            unique_squares.add((guard_position[0], guard_position[1]))

    unique_squares.remove((start_guard_position[0], start_guard_position[1]))

    possible_grids = []
    for row_coord, col_coord in unique_squares:
        if grid[row_coord, col_coord] != '#':
            possible_grid = grid.copy()
            possible_grid[row_coord, col_coord] = '&'

            possible_grids.append(possible_grid)

    count = 0
    for possible_grid in possible_grids:
        path = set([])
        escaped = False
        guard_position = start_guard_position
        direction = start_direction

        while ((guard_position[0], guard_position[1]),
               (direction[0], direction[1])) not in path:
            path.add(((guard_position[0], guard_position[1]),
                      (direction[0], direction[1])))

            # visualise_grid(guard_position, direction, possible_grid)
            potential_next_pos = guard_position + direction

            if (potential_next_pos[0] >= possible_grid.shape[0]
                    or potential_next_pos[0] < 0
                    or potential_next_pos[1] >= possible_grid.shape[1]
                    or potential_next_pos[1] < 0):
                escaped = True
                break

            elif possible_grid[potential_next_pos[0], potential_next_pos[1]] in ('#', '&'):
                direction = rotation @ direction

            else:
                guard_position = potential_next_pos

        if not escaped:
            count += 1

    return count


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as fh:
        contents = fh.read()

    print('Part 1 solution:', part1(contents))
    print('Part 2 solution:', part2(contents))
