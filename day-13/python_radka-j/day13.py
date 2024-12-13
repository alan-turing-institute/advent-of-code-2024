import re

with open("input.txt") as f:
    lines = f.read().splitlines()

# use to parse input into individual machines
indices = [-1] + [i for i, x in enumerate(lines) if x == ""]


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

    # parse input
    if i == len(indices) - 1:
        descript = lines[indices[i] + 1 :]
    else:
        descript = lines[indices[i] + 1 : indices[i + 1]]
    machine = {
        "A": [int(n) for n in re.findall(r"\d+", descript[0])],
        "B": [int(n) for n in re.findall(r"\d+", descript[1])],
        "X": [int(n) for n in re.findall(r"\d+", descript[2])],
    }

    # PART 1
    a, b = solve_system(machine["A"], machine["B"], machine["X"])
    if (a).is_integer() and (b).is_integer():
        tot1 += 3 * a + b

    # PART 2
    machine["X"][0] += 10000000000000
    machine["X"][1] += 10000000000000
    a, b = solve_system(machine["A"], machine["B"], machine["X"])
    if (a).is_integer() and (b).is_integer():
        tot2 += 3 * a + b


print(tot1)
print(tot2)
