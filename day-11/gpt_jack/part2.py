from collections import defaultdict


def evolve_stones_grouped(initial_stones, blinks):
    """
    Evolve the stones by grouping them based on unique characteristics.
    """
    # Count stones based on their values
    stone_counts = defaultdict(int)
    for stone in initial_stones:
        stone_counts[stone] += 1

    for _ in range(blinks):
        new_stone_counts = defaultdict(int)
        for stone, count in stone_counts.items():
            if stone == 0:
                # Rule: 0 becomes 1
                new_stone_counts[1] += count
            elif len(str(stone)) % 2 == 0:
                # Rule: Stones with even digits split
                mid = len(str(stone)) // 2
                left = int(str(stone)[:mid])
                right = int(str(stone)[mid:])
                new_stone_counts[left] += count
                new_stone_counts[right] += count
            else:
                # Rule: Stones with odd digits multiply by 2024
                new_stone_counts[stone * 2024] += count
        stone_counts = new_stone_counts

    # Sum the counts to get the total number of stones
    return sum(stone_counts.values())


def main():
    # Read the input from the file
    with open("input.txt", "r") as file:
        input_data = file.read().strip()

    # Parse the initial arrangement of stones
    stones = list(map(int, input_data.split()))

    # Number of blinks to simulate
    blinks = 75

    # Evolve the stones
    total_stones = evolve_stones_grouped(stones, blinks)

    # Output the total number of stones
    print(total_stones)


if __name__ == "__main__":
    main()
