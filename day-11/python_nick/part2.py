TEST = False

if TEST:
    test_input = "125 17"
else:
    test_input = open("input.txt").read().strip()
stones = test_input.split()

cache = {}

def strip_leading_zeros(stone):
    while stone.startswith("0"):
        stone = stone[1:]
    if len(stone) == 0:
        stone = "0"
    return stone


def apply_rules_to_stone(stone, num_remaining_steps):
    if stone in cache:
        if num_steps in cache[stone]:
            return cache[stone][num_remaining_steps]
    else:
        cache[stone] = {}
    if num_steps == 0:
        return 1
    new_stones = []
    if stone == "0":
        new_stones.append("1")
    elif len(stone) % 2 == 0:
        first_half = strip_leading_zeros(stone[:len(stone)//2])
        second_half = strip_leading_zeros(stone[len(stone)//2:])
        new_stones.append(first_half)
        new_stones.append(second_half)
    else:
        new_stones.append(str(int(stone)*2024))
    total =0
    for new_stone in new_stones:
        total += apply_rules_to_stone(new_stone, num_remaining_steps-1)
    cache[stone][num_steps] = total
    return total


total = 0
for stone in stones:
    total += apply_rules_to_stone(stone, 75)

print(f"Part 2: {total}")
