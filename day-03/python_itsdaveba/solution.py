import re
import numpy as np

# Read input
with open("input.txt") as file:
    input = file.read()


# Part One

num_pattern = r"\d{1,3}"  # Match 1-3 digit numbers
pattern = r"mul\({0},{0}\)".format(num_pattern)  # Match `mul(X,Y)`, where `X` and `Y` are each 1-3 digit numbers
num_p = re.compile(num_pattern)
p = re.compile(pattern)

result = 0
for match in p.findall(input):  # mul(X,Y)
    nums = np.array(num_p.findall(match), dtype=int)  # array[X, Y]
    result += nums.prod()  # X * Y

print("Part One:", result)


# Part Two

# Match `mul(X,Y)`, where `X` and `Y` are each 1-3 digit numbers OR `do()` OR `don't()`
pattern = r"mul\({0},{0}\)|do(n't)?\(\)".format(num_pattern)
p = re.compile(pattern)

result = 0
enabled = True
for match in p.finditer(input):
    match = match.group()
    char = match[2]  # Check third character
    if char == "(":  # `do()`
        enabled = True
    elif char == "n":  # `don't()`
        enabled = False
    elif enabled:
        nums = np.array(num_p.findall(match), dtype=int)  # array[X, Y]
        result += nums.prod()  # X * Y

print("Part Two:", result)
