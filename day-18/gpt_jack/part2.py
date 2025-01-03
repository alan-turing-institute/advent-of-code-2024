from collections import deque


def read_input(file_path):
    """Reads the input file and returns a list of (x, y) coordinates."""
    with open(file_path, "r") as f:
        lines = f.readlines()
    return [tuple(map(int, line.strip().split(","))) for line in lines]


def get_grid_size(byte_positions):
    """Determines the required grid size based on the input byte positions."""
    max_x = max(x for x, _ in byte_positions)
    max_y = max(y for _, y in byte_positions)
    return max_x + 1, max_y + 1  # +1 to include the boundary


def simulate_corruption(byte_positions, grid_width, grid_height, steps_to_simulate):
    """Simulates the memory corruption based on the falling bytes."""
    grid = [[False] * grid_width for _ in range(grid_height)]

    for i, (x, y) in enumerate(byte_positions):
        if i >= steps_to_simulate:
            break
        if 0 <= x < grid_width and 0 <= y < grid_height:
            grid[y][x] = True

    return grid


def find_shortest_path(grid, start, end):
    """Finds the shortest path using BFS on the grid from start to end."""
    grid_height = len(grid)
    grid_width = len(grid[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    queue = deque([(start[0], start[1], 0)])  # (x, y, steps)
    visited = set()
    visited.add((start[0], start[1]))

    while queue:
        x, y, steps = queue.popleft()

        # If we reach the end, return the number of steps
        if (x, y) == end:
            return steps

        # Explore neighbors
        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if (
                0 <= nx < grid_width
                and 0 <= ny < grid_height
                and not grid[ny][nx]
                and (nx, ny) not in visited
            ):
                visited.add((nx, ny))
                queue.append((nx, ny, steps + 1))

    # If no path is found
    return -1


def find_blocking_byte(byte_positions, grid_width, grid_height):
    """Finds the first byte that blocks the path to the exit."""
    grid = [[False] * grid_width for _ in range(grid_height)]
    start = (0, 0)
    end = (grid_width - 1, grid_height - 1)

    for i, (x, y) in enumerate(byte_positions):
        if 0 <= x < grid_width and 0 <= y < grid_height:
            grid[y][x] = True

        # Check if the path to the exit is still reachable
        if find_shortest_path(grid, start, end) == -1:
            return x, y

    return None  # If no byte blocks the path


def main():
    input_file = "input.txt"

    byte_positions = read_input(input_file)

    # Determine grid size dynamically
    grid_width, grid_height = get_grid_size(byte_positions)

    # Find the blocking byte
    blocking_byte = find_blocking_byte(byte_positions, grid_width, grid_height)

    if blocking_byte:
        print(f"{blocking_byte[0]},{blocking_byte[1]}")
    else:
        print("No byte blocks the path.")


if __name__ == "__main__":
    main()
