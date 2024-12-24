# PARSE INPUT

with open("input.txt") as f:
    lines = f.read().splitlines()

inputs = {}
for line in lines[:90]:
    name, val = line.split(": ")
    inputs[name] = int(val)

operations = {}
for line in lines[91:]:
    input1, operand, input2, _, res = line.split(" ")
    operations[(input1, input2, res)] = operand


# PART 1

while operations:
    for var1, var2, res in operations.copy():
        if var1 in inputs and var2 in inputs:
            input1 = int(inputs[var1])
            input2 = int(inputs[var2])
            operand = operations[(var1, var2, res)]
            if operand == "AND":
                inputs[res] = input1 and input2
            elif operand == "OR":
                inputs[res] = input1 or input2
            elif operand == "XOR":
                inputs[res] = input1 ^ input2

            del operations[(var1, var2, res)]

num = ""
for i in range(45, -1, -1):
    if i < 10:
        num += str(inputs[f"z0{i}"])
    else:
        num += str(inputs[f"z{i}"])

print("part 1: ", int(num, 2))
