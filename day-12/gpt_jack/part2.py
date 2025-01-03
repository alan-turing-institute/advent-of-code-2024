from collections import deque


def read_input_file(filename):
    with open(filename, "r") as file:
        return [line.strip() for line in file.readlines()]


def identify_regions(grid):
    rows, cols = len(grid), len(grid[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    regions = []

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def bfs(start, plant_type):
        queue = deque([start])
        region_cells = []
        visited[start[0]][start[1]] = True

        while queue:
            x, y = queue.popleft()
            region_cells.append((x, y))

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if (
                    0 <= nx < rows
                    and 0 <= ny < cols
                    and not visited[nx][ny]
                    and grid[nx][ny] == plant_type
                ):
                    visited[nx][ny] = True
                    queue.append((nx, ny))

        return region_cells

    for r in range(rows):
        for c in range(cols):
            if not visited[r][c]:
                plant_type = grid[r][c]
                region_cells = bfs((r, c), plant_type)
                regions.append((plant_type, region_cells))

    return regions


def calculate_sides_and_area(region_cells, grid):
    rows, cols = len(grid), len(grid[0])

    # Use sets to track unique continuous horizontal and vertical sides
    horizontal_sides = set()
    vertical_sides = set()

    for x, y in region_cells:
        # Horizontal sides
        if y == 0 or grid[x][y - 1] != grid[x][y]:
            horizontal_sides.add((x, y))
        if y == cols - 1 or grid[x][y + 1] != grid[x][y]:
            horizontal_sides.add((x, y + 1))

        # Vertical sides
        if x == 0 or grid[x - 1][y] != grid[x][y]:
            vertical_sides.add((x, y))
        if x == rows - 1 or grid[x + 1][y] != grid[x][y]:
            vertical_sides.add((x + 1, y))

    # Count unique continuous segments
    def count_continuous_sides(sides, is_horizontal=True):
        side_count = 0
        visited = set()

        for side in sides:
            if side not in visited:
                queue = deque([side])
                visited.add(side)

                while queue:
                    current = queue.popleft()
                    cx, cy = current

                    # Move along the same line (horizontal or vertical)
                    neighbors = []
                    if is_horizontal:
                        neighbors = [(cx, cy + 1), (cx, cy - 1)]
                    else:
                        neighbors = [(cx + 1, cy), (cx - 1, cy)]

                    for nx, ny in neighbors:
                        if (nx, ny) in sides and (nx, ny) not in visited:
                            visited.add((nx, ny))
                            queue.append((nx, ny))

                side_count += 1

        return side_count

    horizontal_count = count_continuous_sides(horizontal_sides, is_horizontal=True)
    vertical_count = count_continuous_sides(vertical_sides, is_horizontal=False)

    sides = horizontal_count + vertical_count

    # Area is the number of cells in the region
    area = len(region_cells)

    return area, sides


def calculate_total_price(grid):
    regions = identify_regions(grid)
    total_price = 0

    for plant_type, region_cells in regions:
        area, sides = calculate_sides_and_area(region_cells, grid)
        total_price += area * sides

    return total_price


def main():
    input_file = "input.txt"
    garden_map = read_input_file(input_file)
    total_price = calculate_total_price(garden_map)
    print(f"Total price for fencing all regions: {total_price}")


if __name__ == "__main__":
    main()
