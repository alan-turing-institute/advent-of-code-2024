from math import gcd


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
        n = len(positions)
        if n < 2:
            continue  # No antinodes if less than two antennas of the same frequency

        # Add all antennas as potential antinodes
        for pos in positions:
            antinode_positions.add(pos)

        # For every pair of antennas, calculate all antinodes
        for i in range(n):
            for j in range(i + 1, n):
                x1, y1 = positions[i]
                x2, y2 = positions[j]

                # Calculate the differences
                dx = x2 - x1
                dy = y2 - y1
                gcd_dx_dy = gcd(dx, dy)  # Normalize the direction vector
                dx //= gcd_dx_dy
                dy //= gcd_dx_dy

                # Iterate over all grid points to check if they lie on the line
                for y in range(rows):
                    for x in range(cols):
                        # Check if the point (x, y) satisfies the line equation
                        if (y - y1) * (x2 - x1) == (x - x1) * (y2 - y1):
                            antinode_positions.add((x, y))

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
