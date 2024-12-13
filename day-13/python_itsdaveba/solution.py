import re
import numpy as np

with open("input.txt") as file:
    input = file.read()

configurations = input.split("\n\n")
COST_BTN = (3, 1)  # cost of button (A, B)
CORRECTION = 10000000000000


x_pattern = r"X[+=]\d+"
y_pattern = r"Y[+=]\d+"
x_p = re.compile(x_pattern)
y_p = re.compile(y_pattern)


def find_num_tokens(configurations, correction=0):
    num_tokens = 0
    for configuration in configurations:
        x_axis = x_p.findall(configuration)
        x_axis = [int(x[2:]) for x in x_axis]
        y_axis = y_p.findall(configuration)
        y_axis = [int(y[2:]) for y in y_axis]
        a = [x_axis[:2], y_axis[:2]]
        b = [x_axis[-1] + correction, y_axis[-1] + correction]
        solution = np.linalg.solve(a, b).round(2)
        if all((solution >= 0) & (np.isclose(solution % 1, 0, atol=0.01))):
            num_tokens += np.sum(solution * COST_BTN).astype(int)
    return num_tokens


print("Part One:", find_num_tokens(configurations))
print("Part Two:", find_num_tokens(configurations, correction=CORRECTION))
