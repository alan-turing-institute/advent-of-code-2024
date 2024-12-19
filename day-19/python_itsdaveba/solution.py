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
