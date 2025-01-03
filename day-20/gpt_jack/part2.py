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


def bfs_with_path(grid, start, end):
    """Compute shortest path from start to end and return both the path and distances."""
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    distances = {}
    parents = {}
    queue = deque([(0, start[0], start[1])])  # (distance, r, c)
    visited = set()

    while queue:
        dist, r, c = queue.popleft()
        if (r, c) in visited:
            continue
        visited.add((r, c))
        distances[(r, c)] = dist

        if (r, c) == end:
            break

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if (
                is_valid(grid, nr, nc)
                and grid[nr][nc] != "#"
                and (nr, nc) not in visited
            ):
                queue.append((dist + 1, nr, nc))
                parents[(nr, nc)] = (r, c)

    # Reconstruct the path
    path = []
    current = end
    while current in parents:
        path.append(current)
        current = parents[current]
    path.append(start)
    path.reverse()

    return distances, path


def evaluate_path_cheats(grid, path, max_cheat_time):
    """Evaluate possible cheats along the optimal path."""
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    cheats = {}

    for i in range(len(path) - 1):
        start_segment = path[i]
        end_segment = path[i + 1]

        # Check if a wall separates the segment
        for dr, dc in directions:
            wall_r, wall_c = start_segment[0] + dr, start_segment[1] + dc
            if is_valid(grid, wall_r, wall_c) and grid[wall_r][wall_c] == "#":
                # Temporarily remove the wall
                grid[wall_r][wall_c] = "."

                # Check if the segment can be directly connected
                new_distances, _ = bfs_with_path(grid, path[0], path[-1])
                grid[wall_r][wall_c] = "#"  # Restore the wall

                if end_segment in new_distances:
                    savings = new_distances[end_segment] - (i + 1)
                    if savings > 0 and savings <= max_cheat_time:
                        cheats[(wall_r, wall_c)] = savings

    return cheats


def count_cheats_saving_at_least(grid, start, end, threshold, max_cheat_time):
    distances, path = bfs_with_path(grid, start, end)

    if end not in distances:
        return 0  # No valid path exists

    normal_time = distances[end]
    cheats = evaluate_path_cheats(grid, path, max_cheat_time)

    return sum(1 for cheat in cheats.values() if cheat >= threshold)


def main():
    grid = parse_input("input.txt")
    start, end = find_positions(grid)
    threshold = 100
    max_cheat_time = 20
    result = count_cheats_saving_at_least(grid, start, end, threshold, max_cheat_time)
    print(result)


if __name__ == "__main__":
    main()
