import re
import math
import numpy as np

test_input = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""

regexps = [
    re.compile("Button A: X\+([\d]+), Y\+([\d]+)"),
    re.compile("Button B: X\+([\d]+), Y\+([\d]+)"),
    re.compile("Prize: X=([\d]+), Y=([\d]+)")
]
labels = ["A" , "B", "Prize"]

def parse_input(test=False):
    machines = []
    if test:
        machine_list = test_input.split("\n\n")
    else:
        machine_list = open("input.txt").read().split("\n\n")
    for machine in machine_list:
        machine_dict = {}
        for i, line in enumerate(machine.split("\n")):
            if len(line.strip()) ==0:
                continue
            matches = regexps[i].search(line).groups()
            machine_dict[labels[i]] = [int(match) for match in matches]
        machines.append(machine_dict)
    return machines


def check_integer(number):
    # somehow float.is_integer() seems to give false negatives sometimes
    return abs(number - int(number)) < 1e-5 or abs(number - math.ceil(number)) < 1e-5


def solve_machine(machine_dict):
    lhs = np.array([[machine_dict["A"][0], machine_dict["B"][0]], [machine_dict["A"][1], machine_dict["B"][1]]])
    rhs = np.array([machine_dict["Prize"][0], machine_dict["Prize"][1]])
    result = np.linalg.solve(lhs, rhs)
    if check_integer(result[0]) and result[0] < 100 and check_integer(result[1]) and result[1] < 100:
        return 3 * result[0] + result[1]
    else:
        return 0


machines = parse_input(False)
total = 0
for i, machine in enumerate(machines):
    total += solve_machine(machine)

print(f"Part 1: {total}")
