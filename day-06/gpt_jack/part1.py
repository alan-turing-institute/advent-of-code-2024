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


def simulate_guard(grid):
    directions = ["^", ">", "v", "<"]  # Clockwise order of directions
    dir_map = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}
    visited = set()

    # Find the initial position and direction of the guard
    row, col, current_dir = find_guard_position_and_direction(grid)
    visited.add((row, col))

    while True:
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
                visited.add((row, col))
            else:
                # Guard has moved out of bounds
                break

    return len(visited)


if __name__ == "__main__":
    grid = read_input("input.txt")
    result = simulate_guard(grid)
    print("Distinct positions visited:", result)
