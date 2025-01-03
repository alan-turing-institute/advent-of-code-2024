import heapq


def parse_input(file):
    with open(file, "r") as f:
        maze = [list(line.strip()) for line in f.readlines()]
    start, end = None, None
    for r, row in enumerate(maze):
        for c, val in enumerate(row):
            if val == "S":
                start = (r, c)
            elif val == "E":
                end = (r, c)
    return maze, start, end


def heuristic(position, goal):
    """Manhattan distance heuristic."""
    return abs(position[0] - goal[0]) + abs(position[1] - goal[1])


def get_neighbors(position, direction, maze):
    """Generate valid neighbors and possible transitions."""
    rows, cols = len(maze), len(maze[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # East, South, West, North
    neighbors = []

    # Move forward
    new_pos = (
        position[0] + directions[direction][0],
        position[1] + directions[direction][1],
    )
    if (
        0 <= new_pos[0] < rows
        and 0 <= new_pos[1] < cols
        and maze[new_pos[0]][new_pos[1]] != "#"
    ):
        neighbors.append((new_pos, direction, 1))  # (position, direction, cost)

    # Rotate clockwise and counterclockwise
    neighbors.append((position, (direction + 1) % 4, 1000))  # Clockwise rotation
    neighbors.append((position, (direction - 1) % 4, 1000))  # Counterclockwise rotation

    return neighbors


def find_lowest_score(maze, start, end):
    """Use A* to find all shortest paths from start to end."""
    pq = []  # Priority queue: (total_cost, position, direction, path_cost)
    heapq.heappush(
        pq, (0 + heuristic(start, end), start, 0, 0)
    )  # Start facing East (0)
    shortest_paths = {}  # Track predecessors for path reconstruction
    shortest_path_length = float("inf")
    shortest_costs = {}  # Track shortest cost to each (position, direction)

    while pq:
        total_cost, current_pos, direction, path_cost = heapq.heappop(pq)

        if (current_pos, direction) in shortest_costs and path_cost > shortest_costs[
            (current_pos, direction)
        ]:
            continue

        if (current_pos, direction) not in shortest_costs or path_cost < shortest_costs[
            (current_pos, direction)
        ]:
            shortest_costs[(current_pos, direction)] = path_cost
            shortest_paths[(current_pos, direction)] = []

        if current_pos == end:
            shortest_path_length = min(shortest_path_length, path_cost)

        for neighbor, new_direction, move_cost in get_neighbors(
            current_pos, direction, maze
        ):
            new_path_cost = path_cost + move_cost
            if new_path_cost <= shortest_path_length:
                heapq.heappush(
                    pq,
                    (
                        new_path_cost + heuristic(neighbor, end),
                        neighbor,
                        new_direction,
                        new_path_cost,
                    ),
                )
                if new_path_cost <= shortest_costs.get(
                    (neighbor, new_direction), float("inf")
                ):
                    if new_path_cost < shortest_costs.get(
                        (neighbor, new_direction), float("inf")
                    ):
                        shortest_paths[(neighbor, new_direction)] = []
                    shortest_paths[(neighbor, new_direction)].append(
                        ((current_pos, direction), path_cost)
                    )

    return shortest_paths, shortest_path_length


def find_best_path_tiles(shortest_paths, start, end):
    """Count all tiles appearing in any of the shortest paths."""
    best_tiles = set()
    stack = [
        (end, d) for d in range(4)
    ]  # Start backtracking from all directions at the end

    while stack:
        current, direction = stack.pop()
        if (current, direction) in best_tiles:
            continue

        best_tiles.add((current, direction))
        for (predecessor, pred_dir), _ in shortest_paths.get((current, direction), []):
            stack.append((predecessor, pred_dir))

    # Ensure the start tile is included
    best_tiles_positions = {pos for pos, _ in best_tiles}
    if start not in best_tiles_positions:
        best_tiles_positions.add(start)

    return best_tiles_positions


def main():
    maze, start, end = parse_input("input.txt")
    shortest_paths, shortest_path_length = find_lowest_score(maze, start, end)
    best_tiles = find_best_path_tiles(shortest_paths, start, end)

    # Mark the best path tiles on the maze
    for r, row in enumerate(maze):
        for c, val in enumerate(row):
            if (r, c) in best_tiles:
                maze[r][c] = "O"

    for row in maze:
        print("".join(row))

    print(f"Number of tiles on the best paths: {len(best_tiles)}")


if __name__ == "__main__":
    main()
