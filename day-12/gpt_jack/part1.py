from collections import deque


def read_input_file(filename):
    with open(filename, "r") as file:
        return [line.strip() for line in file.readlines()]


def calculate_area_and_perimeter(grid, visited, start, plant_type):
    rows, cols = len(grid), len(grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    queue = deque([start])
    visited[start[0]][start[1]] = True

    area = 0
    perimeter = 0

    while queue:
        x, y = queue.popleft()
        area += 1

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < rows and 0 <= ny < cols:
                if grid[nx][ny] == plant_type and not visited[nx][ny]:
                    visited[nx][ny] = True
                    queue.append((nx, ny))
                elif grid[nx][ny] != plant_type:
                    perimeter += 1
            else:
                perimeter += 1

    return area, perimeter


def calculate_total_price(grid):
    rows, cols = len(grid), len(grid[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]

    total_price = 0

    for r in range(rows):
        for c in range(cols):
            if not visited[r][c]:
                plant_type = grid[r][c]
                area, perimeter = calculate_area_and_perimeter(
                    grid, visited, (r, c), plant_type
                )
                total_price += area * perimeter

    return total_price


def main():
    input_file = "input.txt"
    garden_map = read_input_file(input_file)
    total_price = calculate_total_price(garden_map)
    print(f"Total price for fencing all regions: {total_price}")


if __name__ == "__main__":
    main()
