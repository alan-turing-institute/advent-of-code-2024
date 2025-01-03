from collections import deque


def parse_input(filename):
    with open(filename, "r") as f:
        grid = [list(line.strip()) for line in f.readlines()]
    return grid


def find_positions(grid):
    start = end = None
    for r, row in enumerate(grid):
        for c, char in enumerate(row):
            if char == "S":
                start = (r, c)
            elif char == "E":
                end = (r, c)
    return start, end


def is_valid(grid, r, c):
    return 0 <= r < len(grid) and 0 <= c < len(grid[0])


def bfs_with_distances(grid, start, end):
    """Compute shortest path distances from start to all reachable points."""
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    distances = {}
    queue = deque([(0, start[0], start[1])])  # (distance, r, c)
    visited = set()

    while queue:
        dist, r, c = queue.popleft()
        if (r, c) in visited:
            continue
        visited.add((r, c))
        distances[(r, c)] = dist

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if is_valid(grid, nr, nc) and grid[nr][nc] != "#":
                queue.append((dist + 1, nr, nc))

    return distances.get(end, float("inf")), distances


def evaluate_wall_removal(grid, r, c, start, end, normal_time):
    """Evaluate the impact of removing a specific wall."""
    # Temporarily remove the wall
    grid[r][c] = "."

    # Recompute the shortest path with the wall removed
    new_time, _ = bfs_with_distances(grid, start, end)

    # Restore the wall
    grid[r][c] = "#"

    # Calculate savings
    return normal_time - new_time if new_time < normal_time else 0


def count_cheats_saving_at_least(grid, start, end, threshold):
    normal_time, _ = bfs_with_distances(grid, start, end)

    if normal_time == float("inf"):
        print("No valid path exists.")
        return 0

    cheats = {}
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == "#":
                # Evaluate the savings for removing this wall
                savings = evaluate_wall_removal(grid, r, c, start, end, normal_time)
                if savings >= threshold:
                    cheats[(r, c)] = savings
                    print(f"Removing wall at ({r}, {c}) saves {savings} picoseconds.")

    print(f"Total cheats saving at least {threshold} picoseconds: {len(cheats)}")
    return len(cheats)


def main():
    grid = parse_input("input.txt")
    start, end = find_positions(grid)
    threshold = 100
    result = count_cheats_saving_at_least(grid, start, end, threshold)
    print(result)


if __name__ == "__main__":
    main()
