from collections import defaultdict

with open("input.txt") as f:
    lines = f.read().splitlines()

split_idx = lines.index("")

# dictionary of {<int>: [<ints that have to follow it in an update>], ...}
rules = defaultdict(list)
for rule in lines[:split_idx]:
    n1, n2 = [int(n) for n in rule.split("|")]
    rules[n1].append(n2)

updates = [[int(n) for n in update.split(",")] for update in lines[split_idx + 1 :]]


# using custom object with a "less than" rule allows us to use internal python sort
class UpdateObj:
    def __init__(self, n):
        self.n = n
        self.n_rules = rules[n]

    def __lt__(self, other):
        if other.n in self.n_rules:
            return True
        return False


good_sum = 0
bad_ordered_sum = 0
for update in updates:
    good = True
    for i, n in enumerate(update):
        # check if any preceding numbers in update have a rule to appear after `n`
        rules_for_n = rules[n]
        if rules_for_n != []:
            for n_prec in update[:i]:
                if n_prec in rules_for_n:
                    good = False
                    break
    if good:
        good_sum += update[len(update) // 2]
    else:
        sorted_update = sorted([UpdateObj(n) for n in update])
        bad_ordered_sum += sorted_update[len(update) // 2].n

print("part 1: ", good_sum)
print("part 2: ", bad_ordered_sum)
