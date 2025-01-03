def evolve_stones(stones, blinks):
    """Evolve the stones over a number of blinks."""
    for _ in range(blinks):
        new_stones = []
        for stone in stones:
            if stone == 0:
                new_stones.append(1)
            elif len(str(stone)) % 2 == 0:  # Even number of digits
                mid = len(str(stone)) // 2
                left = int(str(stone)[:mid])
                right = int(str(stone)[mid:])
                new_stones.extend([left, right])
            else:
                new_stones.append(stone * 2024)
        stones = new_stones
    return stones


def main():
    # Read the input from the file
    with open("input.txt", "r") as file:
        input_data = file.read().strip()

    # Parse the initial arrangement of stones
    stones = list(map(int, input_data.split()))

    # Number of blinks to simulate
    blinks = 25

    # Evolve the stones
    result_stones = evolve_stones(stones, blinks)

    # Output the number of stones after 25 blinks
    print(len(result_stones))


if __name__ == "__main__":
    main()
