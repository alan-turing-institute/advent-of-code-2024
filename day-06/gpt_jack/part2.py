def read_input(file_name):
    with open(file_name, "r") as file:
        return [list(line.strip()) for line in file]


def find_guard_position_and_direction(grid):
    directions = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] in directions:
                return (row, col, grid[row][col])
    return None


def simulate_guard_with_obstruction(grid, obstruction_pos=None):
    directions = ["^", ">", "v", "<"]  # Clockwise order of directions
    dir_map = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}
    visited = set()
    path = set()

    # Place the obstruction if specified
    if obstruction_pos:
        grid[obstruction_pos[0]][obstruction_pos[1]] = "#"

    # Find the initial position and direction of the guard
    row, col, current_dir = find_guard_position_and_direction(grid)
    visited.add((row, col))

    while True:
        # Add current position and direction to path
        path.add((row, col, current_dir))

        # Calculate the next position based on the current direction
        dr, dc = dir_map[current_dir]
        next_row, next_col = row + dr, col + dc

        if (
            0 <= next_row < len(grid)
            and 0 <= next_col < len(grid[0])
            and grid[next_row][next_col] == "#"
        ):
            # Obstacle ahead, turn right
            current_dir = directions[(directions.index(current_dir) + 1) % 4]
        else:
            # Move forward
            if 0 <= next_row < len(grid) and 0 <= next_col < len(grid[0]):
                row, col = next_row, next_col
                if (row, col, current_dir) in path:
                    return True  # Loop detected
                visited.add((row, col))
            else:
                return False  # Guard moved out of bounds


def find_loop_positions(grid):
    loop_positions = set()
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if (
                grid[row][col] == "."
                and (row, col) != find_guard_position_and_direction(grid)[:2]
            ):
                # Simulate guard with the potential new obstruction
                grid_copy = [row[:] for row in grid]
                if simulate_guard_with_obstruction(grid_copy, (row, col)):
                    loop_positions.add((row, col))
    return loop_positions


if __name__ == "__main__":
    grid = read_input("input.txt")
    loop_positions = find_loop_positions(grid)
    print("Number of positions causing a loop:", len(loop_positions))
