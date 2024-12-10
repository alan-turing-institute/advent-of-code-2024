with open("input.txt") as f:
    input_raw = f.read()

# ==================================================
# PART 1
# ==================================================

# format input

ID_count = input_raw[::2]
space = input_raw[1::2]

input = []
for id, n in enumerate(ID_count):
    input.extend([id] * int(n))
    if id < len(space):
        input.extend(["."] * int(space[id]))

# 2 pointers

pointer = len(input) - 1
reordered_input = []
for i, char in enumerate(input):
    if char != ".":
        reordered_input.append(char)
    else:
        reordered_input.append(input[pointer])
        input[pointer] = "."
        # decrement pointer until get to next number
        while input[pointer] == ".":
            pointer -= 1
    if i >= pointer:
        break

tot = 0
for i, val in enumerate(reordered_input):
    tot += val * i

print("part 1: ", tot)

# ==================================================
# PART 2
# - hmmmm.......
# ==================================================

# format input (different to part 1)

ID = 0
input = []
for i, n in enumerate(input_raw):
    if i % 2 == 0:
        input.append([str(ID), int(n)])
        ID += 1
    else:
        input.append([".", int(n)])

# swap blocks

# loop through numbers from the back
for id, size in input[::-1]:
    if id != ".":
        # go through available spaces from the front
        idx_max = input.index([id, size])
        for i, (char, available) in enumerate(input[:idx_max]):
            if char == ".":
                # can move item to this space?
                if size <= available:
                    # decrement amount of free space at pos
                    input[i][1] -= size
                    # insert number in right place and replace it with free space
                    idx = input.index([id, size])
                    input[idx] = [".", size]
                    input.insert(i, [id, size])
                    break

tot = 0
pos = 0
for val, count in input:
    for i in range(count):
        if val != ".":
            tot += int(val) * pos
        pos += 1

print("part 2: ", tot)
