def count_word_occurrences(grid, word):
    """
    Counts the occurrences of the word in all directions in the grid.

    Parameters:
        grid (list of str): The grid of letters as a list of strings.
        word (str): The word to search for.

    Returns:
        int: Total occurrences of the word in the grid.
    """

    def is_valid(x, y):
        """Check if the position (x, y) is within the grid bounds."""
        return 0 <= x < rows and 0 <= y < cols

    def search_from(x, y, dx, dy):
        """Search for the word starting from (x, y) in direction (dx, dy)."""
        for k in range(len(word)):
            nx, ny = x + k * dx, y + k * dy
            if not is_valid(nx, ny) or grid[nx][ny] != word[k]:
                return 0
        return 1

    rows, cols = len(grid), len(grid[0])
    directions = [
        (0, 1),  # Right
        (1, 0),  # Down
        (0, -1),  # Left
        (-1, 0),  # Up
        (1, 1),  # Down-Right
        (1, -1),  # Down-Left
        (-1, 1),  # Up-Right
        (-1, -1),  # Up-Left
    ]

    count = 0
    for x in range(rows):
        for y in range(cols):
            for dx, dy in directions:
                count += search_from(x, y, dx, dy)

    return count


# Read the grid from the input file
def main():
    input_file = "input.txt"  # Replace with your file name
    with open(input_file, "r") as f:
        grid = [line.strip() for line in f]

    word = "XMAS"
    result = count_word_occurrences(grid, word)
    print(f"The word '{word}' appears {result} times in the grid.")


if __name__ == "__main__":
    main()
