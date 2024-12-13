import re

import numpy as np

with open("input.txt") as f:
    lines = f.read().splitlines()

# use to parse input into individual machines
indices = [-1] + [i for i, x in enumerate(lines) if x == ""]


def play_machine(machine, max_button_press):
    target = machine["X"]
    a = machine["A"]
    b = machine["B"]

    cheapest = np.inf
    for i in range(max_button_press):
        for j in range(max_button_press):
            if i * a[0] + j * b[0] == target[0] and i * a[1] + j * b[1] == target[1]:
                price = i * 3 + j
                if price < cheapest:
                    cheapest = price
            if i * a[0] + j * b[0] > target[0] and i * a[1] + j * b[1] > target[1]:
                break
    return cheapest


def solve_system(a, b, target):
    """
    From: https://en.wikipedia.org/wiki/Cramer%27s_rule#Applications
    """
    a1, a2 = a
    b1, b2 = b
    c1, c2 = target
    x = (c1 * b2 - b1 * c2) / (a1 * b2 - b1 * a2)
    y = (a1 * c2 - c1 * a2) / (a1 * b2 - b1 * a2)
    return x, y


tot1 = 0
tot2 = 0
for i in range(len(indices)):
    if i == len(indices) - 1:
        descript = lines[indices[i] + 1 :]
    else:
        descript = lines[indices[i] + 1 : indices[i + 1]]
    machine = {
        "A": [int(n) for n in re.findall(r"\d+", descript[0])],
        "B": [int(n) for n in re.findall(r"\d+", descript[1])],
        "X": [int(n) for n in re.findall(r"\d+", descript[2])],
    }

    # PART 1 - the slow method
    price = play_machine(machine, 100)
    if price < np.inf:
        tot1 += price

    # PART 2 - use math
    machine["X"][0] += 10000000000000
    machine["X"][1] += 10000000000000
    a, b = solve_system(machine["A"], machine["B"], machine["X"])
    if (a).is_integer() and (b).is_integer():
        tot2 += 3 * a + b


print(tot1)
print(tot2)
