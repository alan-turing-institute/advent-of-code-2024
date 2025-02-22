def parse_input(file_name):
    """Reads the input file and parses the topographic map."""
    with open(file_name, "r") as file:
        return [list(map(int, line.strip())) for line in file.readlines()]


def find_trailheads(map_data):
    """Find all trailheads (positions with height 0)."""
    trailheads = []
    for row in range(len(map_data)):
        for col in range(len(map_data[0])):
            if map_data[row][col] == 0:
                trailheads.append((row, col))
    return trailheads


def bfs_score(map_data, start):
    """Performs BFS to calculate the score of reachable 9s from a trailhead."""
    queue = [start]
    visited = set()
    visited.add(start)
    reachable_nines = set()

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        x, y = queue.pop(0)
        current_height = map_data[x][y]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < len(map_data) and 0 <= ny < len(map_data[0]):
                if (nx, ny) not in visited and map_data[nx][ny] == current_height + 1:
                    visited.add((nx, ny))
                    queue.append((nx, ny))

                    if map_data[nx][ny] == 9:
                        reachable_nines.add((nx, ny))

    return len(reachable_nines)


def bfs_rating(map_data, start):
    """Performs BFS to calculate the rating (number of distinct hiking trails) from a trailhead."""
    queue = [(start, [])]  # Queue of (current position, trail path)
    visited = set()
    distinct_trails = set()

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        (x, y), path = queue.pop(0)
        current_height = map_data[x][y]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < len(map_data) and 0 <= ny < len(map_data[0]):
                if map_data[nx][ny] == current_height + 1:
                    new_path = path + [(nx, ny)]
                    if map_data[nx][ny] == 9:
                        distinct_trails.add(tuple(new_path))
                    else:
                        queue.append(((nx, ny), new_path))

    return len(distinct_trails)


def calculate_total_score_and_rating(map_data):
    """Calculates the sum of scores and ratings for all trailheads."""
    trailheads = find_trailheads(map_data)
    total_score = 0
    total_rating = 0

    for trailhead in trailheads:
        total_score += bfs_score(map_data, trailhead)
        total_rating += bfs_rating(map_data, trailhead)

    return total_score, total_rating


def main():
    input_file = "input.txt"
    map_data = parse_input(input_file)
    total_score, total_rating = calculate_total_score_and_rating(map_data)
    print(f"Total score of all trailheads: {total_score}")
    print(f"Total rating of all trailheads: {total_rating}")


if __name__ == "__main__":
    main()
