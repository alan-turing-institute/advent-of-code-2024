import numpy as np

with open("input.txt") as f:
    lines = f.read().splitlines()


blocks = [lines[i : i + 7] for i in range(0, len(lines), 8)]


def count_pins(block):
    pin_heights = [0] * 5
    for row in block:
        for idx in range(5):
            if row[idx] == "#":
                pin_heights[idx] += 1
    return pin_heights


# each block is either a key or a lock based on its direction
keys = []
locks = []
for block in blocks:
    pin_heights = count_pins(block)
    if block[0] == ".....":
        locks.append(pin_heights)
    elif block[-1] == ".....":
        keys.append(pin_heights)

count = 0
for key in keys:
    for lock in locks:
        if np.all(np.array(key) + np.array(lock) <= 7):
            count += 1

print(count)
