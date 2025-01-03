def count_ways_to_form_design(towel_patterns, design):
    """
    Count the number of ways a design can be formed using the given towel patterns.
    """
    n = len(design)
    dp = [0] * (
        n + 1
    )  # dp[i] stores the number of ways to form the first i characters of the design
    dp[0] = 1  # Base case: one way to form an empty design (use no towels)

    for i in range(1, n + 1):
        for pattern in towel_patterns:
            if i >= len(pattern) and design[i - len(pattern) : i] == pattern:
                dp[i] += dp[i - len(pattern)]

    return dp[n]


def main():
    with open("input.txt", "r") as file:
        lines = file.read().strip().split("\n")

    # First line is the towel patterns
    towel_patterns = lines[0].split(", ")

    # Designs are listed after a blank line
    designs = lines[2:]

    # Sum the number of ways for all designs
    total_ways = 0

    for design in designs:
        total_ways += count_ways_to_form_design(towel_patterns, design)

    print(f"Total number of ways: {total_ways}")


if __name__ == "__main__":
    main()
