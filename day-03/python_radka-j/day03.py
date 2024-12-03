import re

with open("input.txt") as f:
    input = f.read()

# PART 1
pattern = r"mul\(\d+,\d+\)"
valid_instructions = re.findall(pattern, input)

total = 0
for instruct in valid_instructions:
    ints = [int(val) for val in re.findall(r"\d+", instruct)]
    total += ints[0] * ints[1]

print("part 1: ", total)

# PART 2
pattern = r"mul\(\d+,\d+\)|do\(\)|don't\(\)"
valid_instructions = re.findall(pattern, input)

total = 0
enabled = True
for instruct in valid_instructions:
    if instruct == "do()":
        enabled = True
    elif instruct == "don't()":
        enabled = False
    else:
        if enabled:
            ints = [int(val) for val in re.findall(r"\d+", instruct)]
            total += ints[0] * ints[1]

print("part 2: ", total)
