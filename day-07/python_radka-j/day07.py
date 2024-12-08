import itertools

with open("input.txt") as f:
    lines = f.read().splitlines()


# can the the vals equal the tot with the right combination of operators?
def can_be_true(vals, tot, operators):
    for comb in itertools.product(operators, repeat=len(vals) - 1):
        res = vals[0]
        for i, n in enumerate(vals[1:]):
            if comb[i] == "+":
                res += n
            elif comb[i] == "*":
                res *= n
            elif comb[i] == "||":
                res = int(str(res) + str(n))
        if res == tot:
            return True
    return False


part1_vals = []
part2_vals = []
for line in lines:
    tot_str, vals_str = line.split(": ")
    tot_int = int(tot_str)
    vals_int = [int(n) for n in vals_str.split(" ")]

    if can_be_true(vals_int, tot_int, operators=["+", "*"]):
        part1_vals.append(tot_int)
    else:
        if can_be_true(vals_int, tot_int, operators=["+", "*", "||"]):
            part2_vals.append(tot_int)

print("part 1: ", sum(part1_vals))
print("part 2: ", sum(part1_vals) + sum(part2_vals))
