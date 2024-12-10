def read_input(filename):
    """Reads the input file and returns a 2D list representation of the map."""
    with open(filename, "r") as file:
        return [list(line.strip()) for line in file.readlines()]


def find_antennas(grid):
    """Finds all antennas and their coordinates in the grid."""
    antennas = {}
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char.isalnum():  # Antennas are alphanumeric
                if char not in antennas:
                    antennas[char] = []
                antennas[char].append((x, y))
    return antennas


def calculate_antinodes(grid, antennas):
    """Calculates the antinodes based on antenna positions."""
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    antinode_positions = set()

    for freq, positions in antennas.items():
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                x1, y1 = positions[i]
                x2, y2 = positions[j]

                # Calculate the vector difference
                dx = x2 - x1
                dy = y2 - y1

                # Calculate the potential antinodes
                ax, ay = x1 - dx, y1 - dy  # Antinode 1
                bx, by = x2 + dx, y2 + dy  # Antinode 2

                # Add valid antinodes within bounds to the set
                if 0 <= ax < cols and 0 <= ay < rows:
                    antinode_positions.add((ax, ay))
                if 0 <= bx < cols and 0 <= by < rows:
                    antinode_positions.add((bx, by))

    return antinode_positions


def count_antinodes(filename):
    """Main function to count unique antinode locations."""
    grid = read_input(filename)
    antennas = find_antennas(grid)
    antinode_positions = calculate_antinodes(grid, antennas)
    return len(antinode_positions)


if __name__ == "__main__":
    input_file = "input.txt"
    result = count_antinodes(input_file)
    print(f"Total unique locations containing an antinode: {result}")
