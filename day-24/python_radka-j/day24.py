from collections import defaultdict

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

# ======================================================================================
# PART 1
# ======================================================================================

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
# highest z value is 45
for i in range(45, -1, -1):
    if i < 10:
        num += str(inputs[f"z0{i}"])
    else:
        num += str(inputs[f"z{i}"])

print("part 1: ", int(num, 2))

# ======================================================================================
# PART 2: ripple adder
#
# to add two binary numbers start with the least significant digit (00) and move to the
# most significant (here 45), at each step have:
# - 3 inputs: the two bits to be added (A and B) and a carry-in from previous step
# - 2 outputs: a sum and carry-out
# where:
#   - sum = a XOR b XOR carry_in
#   - carry_out = (a AND b) OR (carry_in AND (a XOR b))
#
# this is what the gates implement, leading to the following pattern:
#  z00 = x00 XOR y00                  # no carry_in at first step
#
#  z01 = jfw XOR gnj                  # sum of inputs at n=1 and carry_in from n=0
#       gnj = y01 XOR x01             #
#       jfw = x00 AND y00             # carry_in (only the left hand side of OR in the
#                                     # carry formula since there was no carry_in at 0)
#
#   z02 = ndd XOR jgw                 # sum of inputs at n=2 and carry_in from n=1
#       jgw = y02 XOR x02             #
#       ndd = ntt OR spq              # carry-in
#           ntt = x01 AND y01         # left hand side of OR in carry formula
#           spq = gnj AND jfw         # right hand side of OR in carry formula
#
#  ...everything else should be as z02...
#
# we can derive some rules from above (at least for gates z02-z44)
# ======================================================================================


# recreate operations iterable since it's been deleted in part 1
operations = []
# also keep a simple look-up table of inputs and operations/gates they are passed to
input_operand_map = defaultdict(list)
for line in lines[91:]:
    input1, operand, input2, _, res = line.split(" ")
    operations.append([input1, input2, res, operand])
    input_operand_map[input1].append(operand)
    input_operand_map[input2].append(operand)

# keep track of grates that don't follow expected pattern
wrong_gates = set()
for input1, input2, res, operand in operations:
    # lets ignore first and last gates to begin with since they are slightly different
    if not res in ["z00", "z01", "z45"]:

        # 1. expect z gates to results from an XOR
        if res[0] == "z" and operand != "XOR":
            wrong_gates.add(res)

        # 2. if see an XOR, either expect to have x/y inputs or z outputs
        if operand == "XOR":
            if (
                not input1[0] in ["x", "y"]
                and not input2[0] in ["x", "y"]
                and res[0] not in ["z"]
            ):
                wrong_gates.add(res)

        # 3. if have an AND operation then expect that to feed into an OR
        # (the only exception is the operation on the first 2 inputs)
        if operand == "AND":
            if input1 not in ["x00", "y00"] and input2 not in ["x00", "y00"]:
                if "OR" not in input_operand_map[res]:
                    print("check AND", input_operand_map[res])
                    wrong_gates.add(res)

        # 4. an XOR result can feed into another XOR or an AND but not an OR operation
        # (the inputs to OR are only results of AND operations)
        if operand == "XOR":
            if "OR" in input_operand_map[res]:
                print("check XOR", input_operand_map[res])
                wrong_gates.add(res)

print("part 2: ", ",".join(sorted(wrong_gates)))
