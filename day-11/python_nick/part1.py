
TEST = False

if TEST:
    test_input = "125 17"
else:
    test_input = open("input.txt").read().strip()
stones = test_input.split()

def strip_leading_zeros(stone):
    while stone.startswith("0"):
        stone = stone[1:]
    if len(stone) == 0:
        stone = "0"
    return stone


def apply_rules(stones):
    new_stones = []
    for stone in stones:
        if stone == "0":
            new_stones.append("1")
        elif len(stone) % 2 == 0:
            first_half = strip_leading_zeros(stone[:len(stone)//2])
            second_half = strip_leading_zeros(stone[len(stone)//2:])
            new_stones.append(first_half)
            new_stones.append(second_half)
        else:
            new_stones.append(str(int(stone)*2024))
    return new_stones


for _ in range(25):
    stones = apply_rules(stones)

print(f"Part 1: {len(stones)}")
