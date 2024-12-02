from collections import Counter
with open("input.txt") as file:
    lines = [line.strip().split(" ") for line in file]

lhs = [int(line[0]) for line in lines]
rhs = [int(line[-1]) for line in lines]

part1 = sum([max(a, b) - min(a, b) for a, b in zip(sorted(lhs), sorted(rhs))])
print(f"Part 1 = {part1}")

rhs_freq = Counter(rhs)
part2 = sum([x * rhs_freq.get(x, 0) for x in lhs])
print(f"Part 2 = {part2}")