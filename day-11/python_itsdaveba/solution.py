import math

with open("input.txt") as file:
    input = file.read()

stones = list(map(int, input.split()))
total_stones = {}  # stone: list of num of stones after i + 1 blinks
next_stones = {}  # stone: tuple of next stones


def find_total_stones(stone, num_blinks):
    if stone not in next_stones:
        num_digits = math.floor(math.log10(stone)) + 1 if stone > 0 else 0
        if stone == 0:
            next_stones[stone] = (1,)
        elif num_digits % 2 == 0:
            next_stones[stone] = divmod(stone, 10 ** (num_digits // 2))
        else:
            next_stones[stone] = (stone * 2024,)

    if num_blinks != 1:
        for next_stone in next_stones[stone]:
            if next_stone not in total_stones or len(total_stones[next_stone]) < num_blinks - 1:
                find_total_stones(next_stone, num_blinks - 1)

    if stone not in total_stones:
        total_stones[stone] = [len(next_stones[stone])]

    for num_blinks in range(len(total_stones[stone]) - 1, num_blinks - 1):
        total_stones[stone].append(sum([total_stones[next_stone][num_blinks] for next_stone in next_stones[stone]]))

    return total_stones[stone][-1]


print("Part One:", sum([find_total_stones(stone, 25) for stone in stones]))
print("Part Two:", sum([find_total_stones(stone, 75) for stone in stones]))
