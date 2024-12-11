from collections import defaultdict

input_str = "125 17"


# ==================================
# PART 1
# ==================================


def advance_stone(stone, n_max):
    stack = [(stone, 1)]
    count = 1
    while stack:
        curr_stone, n_step = stack.pop()
        if n_step <= n_max:
            n_step += 1
            if curr_stone == "0":
                stack.append(("1", n_step))
            elif len(curr_stone) % 2 == 0:
                idx = len(curr_stone) // 2
                n1 = str(int(curr_stone[:idx]))
                n2 = str(int(curr_stone[idx:]))
                stack.append((n1, n_step))
                stack.append((n2, n_step))
                count += 1
            else:
                stack.append((str(int(curr_stone) * 2024), n_step))
    return count


count = 0
for stone in input_str.split(" "):
    count += advance_stone(stone, 25)

print("part 1: ", count)


# ==================================
# PART 2
# ==================================


stones = input_str.split(" ")
counts = defaultdict(int)
for stone in stones:
    counts[stone] += 1

for _ in range(75):
    temp = defaultdict(int)
    for stone, count in counts.items():
        if stone == "0":
            temp["1"] += count
        elif len(stone) % 2 == 0:
            idx = len(stone) // 2
            n1 = str(int(stone[:idx]))
            n2 = str(int(stone[idx:]))
            temp[n1] += count
            temp[n2] += count
        else:
            new_stone = str(int(stone) * 2024)
            temp[new_stone] += count
    counts = temp

count = 0
for c in counts.values():
    count += c

print("part 2: ", count)
