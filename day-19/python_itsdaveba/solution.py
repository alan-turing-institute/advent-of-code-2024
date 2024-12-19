with open("input.txt") as file:
    input = file.read()

patterns, designs = input.split("\n\n")
patterns = set(patterns.split(", "))
designs = designs.splitlines()

possible = {"": 1}  # design, num_ways
max_pattern_length = max(map(len, patterns))


def num_possible_ways(design):
    counter = 0
    for i in range(1, min(max_pattern_length, len(design)) + 1):
        if design[:i] in patterns:
            if design[i:] not in possible:
                possible[design[i:]] = num_possible_ways(design[i:])
            counter += possible[design[i:]]
    return counter


solution = list(map(num_possible_ways, designs))

print("Part One:", sum(map(bool, solution)))
print("Part Two:", sum(solution))
