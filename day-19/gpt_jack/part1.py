def can_form_design(towel_patterns, design):
    """
    Check if a design can be formed using the given towel patterns using DP.
    """
    n = len(design)
    dp = [False] * (
        n + 1
    )  # dp[i] indicates if the first i characters of the design can be formed
    dp[0] = True  # Base case: empty string can always be formed

    for i in range(1, n + 1):
        for pattern in towel_patterns:
            if i >= len(pattern) and design[i - len(pattern) : i] == pattern:
                if dp[i - len(pattern)]:
                    dp[i] = True
                    break  # No need to check further if we've already formed the prefix

    return dp[n]


def main():
    with open("input.txt", "r") as file:
        lines = file.read().strip().split("\n")

    # First line is the towel patterns
    towel_patterns = lines[0].split(", ")

    # Designs are listed after a blank line
    designs = lines[2:]

    # Count the number of possible designs
    possible_count = 0

    for design in designs:
        if can_form_design(towel_patterns, design):
            possible_count += 1

    print(f"Number of possible designs: {possible_count}")


if __name__ == "__main__":
    main()
