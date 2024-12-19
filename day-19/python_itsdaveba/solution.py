with open("input.txt") as file:
    input = file.read()

patterns, designs = input.split("\n\n")
patterns = set(patterns.split(", "))
max_pattern_length = max(map(len, patterns))
designs = designs.splitlines()
impossible = set()


def is_possible(design):
    for i in range(1, min(max_pattern_length, len(design)) + 1):
        if design[:i] in patterns and design[i:] not in impossible:
            if design[i:] == "" or is_possible(design[i:]):
                return True
    impossible.add(design)
    return False


print("Part One:", sum(map(is_possible, designs)))
    input = file.read()

patterns, designs = input.split("\n\n")
patterns = patterns.split(", ")
designs = designs.splitlines()


def is_possible(design):
    if design == "":
        return True
    for pattern in patterns:
        if design.startswith(pattern):
            if is_possible(design[len(pattern):]):
                return True
    return False


possible = 0
for design in designs:
    if is_possible(design):
        possible += 1

print("Part One:", possible)


# arrange towels
# pattern of colored stripes
# stripe can be [w]hite, bl[u]e, [b]lack, [r]ed or [g]reen
# you can't reverse the pattern
# list of designs
