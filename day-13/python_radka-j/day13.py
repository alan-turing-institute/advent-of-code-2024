import re

import numpy as np

with open("input.txt") as f:
    lines = f.read().splitlines()

# use to parse input into individual machines
breaks = [-1] + [i for i, x in enumerate(lines) if x == ""]


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


tot1 = 0
tot2 = 0
for i in range(len(breaks)):
    if i == len(breaks) - 1:
        descript = lines[breaks[i] + 1 :]
    else:
        descript = lines[breaks[i] + 1 : breaks[i + 1]]
    machine = {
        "A": [int(n) for n in re.findall(r"\d+", descript[0])],
        "B": [int(n) for n in re.findall(r"\d+", descript[1])],
        "X": [int(n) for n in re.findall(r"\d+", descript[2])],
    }

    # PART 1
    price = play_machine(machine, 100)
    if price < np.inf:
        tot1 += price

    # PART 2
    machine["X"][0] += 10000000000000
    machine["X"][1] += 10000000000000
    buttons = np.array(
        [[machine["A"][0], machine["B"][0]], [machine["A"][1], machine["B"][1]]]
    )
    target = np.array(machine["X"])
    a, b = np.linalg.solve(buttons, target)
    if (a).is_integer() and (b).is_integer():
        tot2 += 3 * a + b
    else:
        # hmmmm....
        a_clip = round(a, 4)
        b_clip = round(b, 4)
        if (a_clip).is_integer() and (b_clip).is_integer():
            tot2 += 3 * a_clip + b_clip

print(tot1)
print(tot2)
