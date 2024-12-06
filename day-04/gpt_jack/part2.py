def count_xmas_pattern(grid):
    """
    Counts the occurrences of the X-MAS pattern in the grid, ensuring the center is always 'A'
    and both diagonals match either 'MAS' or 'SAM'.
    """

    def is_valid(x, y):
        """Check if the position (x, y) is within the grid bounds."""
        return 0 <= x < rows and 0 <= y < cols

    def check_xmas(x, y):
        """
        Check if an X-MAS pattern exists centered at (x, y).
        Returns 1 if found, 0 otherwise.
        """
        # Ensure the center is 'A'
        if grid[x][y] != "A":
            return 0

        # Diagonal positions around the center
        top_left = (x - 1, y - 1)
        top_right = (x - 1, y + 1)
        bottom_left = (x + 1, y - 1)
        bottom_right = (x + 1, y + 1)

        # Ensure all diagonal positions are valid
        if not all(
            is_valid(px, py)
            for px, py in [top_left, top_right, bottom_left, bottom_right]
        ):
            return 0

        # Check both diagonals
        diag1 = [
            grid[top_left[0]][top_left[1]],  # Top-left
            grid[x][y],  # Center ('A')
            grid[bottom_right[0]][bottom_right[1]],  # Bottom-right
        ]
        diag2 = [
            grid[top_right[0]][top_right[1]],  # Top-right
            grid[x][y],  # Center ('A')
            grid[bottom_left[0]][bottom_left[1]],  # Bottom-left
        ]

        # Both diagonals must be 'MAS' or 'SAM'
        valid_patterns = [["M", "A", "S"], ["S", "A", "M"]]
        if diag1 in valid_patterns and diag2 in valid_patterns:
            return 1
        return 0

    rows, cols = len(grid), len(grid[0])
    count = 0

    # Search for X-MAS patterns in the grid
    for x in range(1, rows - 1):  # Avoid edges
        for y in range(1, cols - 1):  # Avoid edges
            count += check_xmas(x, y)

    return count


# Read the grid and process
def main():
    input_file = "input.txt"  # Input file name
    try:
        with open(input_file, "r") as f:
            grid = [line.strip() for line in f]
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        return

    result = count_xmas_pattern(grid)
    print(f"The X-MAS pattern appears {result} times in the grid.")


if __name__ == "__main__":
    main()
