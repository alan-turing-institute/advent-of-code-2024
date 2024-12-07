import itertools

with open("input.txt") as f:
    lines = f.read().splitlines()


# can the the vals equal the tot with the right combination of operators?
def can_be_true(vals, tot, operators):
    for comb in itertools.product(operators, repeat=len(vals) - 1):
        val = vals[0]
        for i, n in enumerate(vals[1:]):
            if comb[i] == "+":
                val += n
            elif comb[i] == "*":
                val *= n
            elif comb[i] == "||":
                val = int(str(val) + str(n))
        if val == int(tot):
            return True
    return False


part1_vals = []
part2_vals = []
for line in lines:
    tot, nums = line.split(": ")
    str_vals = nums.split(" ")
    int_vals = [int(n) for n in str_vals]

    if can_be_true(int_vals, int(tot), operators=["+", "*"]):
        part1_vals.append(int(tot))
    else:
        if can_be_true(int_vals, int(tot), operators=["+", "*", "||"]):
            part2_vals.append(int(tot))

print("part 1: ", sum(part1_vals))
print("part 2: ", sum(part1_vals) + sum(part2_vals))
