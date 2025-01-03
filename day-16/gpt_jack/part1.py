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
    """Use A* to find the lowest score from start to end."""
    pq = []  # Priority queue: (total_cost, position, direction, path_cost)
    heapq.heappush(
        pq, (0 + heuristic(start, end), start, 0, 0)
    )  # Start facing East (0)
    visited = set()

    while pq:
        total_cost, current_pos, direction, path_cost = heapq.heappop(pq)

        if (current_pos, direction) in visited:
            continue

        visited.add((current_pos, direction))

        if current_pos == end:
            return path_cost

        for neighbor, new_direction, move_cost in get_neighbors(
            current_pos, direction, maze
        ):
            if (neighbor, new_direction) not in visited:
                new_path_cost = path_cost + move_cost
                heapq.heappush(
                    pq,
                    (
                        new_path_cost + heuristic(neighbor, end),
                        neighbor,
                        new_direction,
                        new_path_cost,
                    ),
                )

    return float("inf")  # If no path is found


def main():
    maze, start, end = parse_input("input.txt")
    lowest_score = find_lowest_score(maze, start, end)
    print(f"The lowest score a Reindeer could possibly get is: {lowest_score}")


if __name__ == "__main__":
    main()
