with open("input.txt") as f:
    lines = f.read().splitlines()

towels = lines[0].split(", ")
patterns = lines[2:]


# =====================================================
# PART 1
# =====================================================


def can_form(pattern, towels):
    """
    Create a dictionary of all possible subpatterns to check (bool values):
        - start with an empty string
        - then just the first character
        - just the first 2 characters
        - ...

    Then loop through each subpattern and at each step:
        - check whether the subpattern ends with one of the towel strings
        - if yes, check whether the subpattern without this towel was also
          valid (i.e., it ended with a towel substring)
        - if both conditions hold, mark this subpattern as valid
    """
    is_valid = {}
    for i in range(len(pattern) + 1):
        is_valid[pattern[:i]] = False
    is_valid[""] = True  # arrangement without any towels is valid

    for subpattern in is_valid:
        for towel in towels:
            if subpattern.endswith(towel):
                previous_subpattern = subpattern.removesuffix(towel)
                if is_valid[previous_subpattern]:
                    is_valid[subpattern] = True
                    # found a towel that makes sub_pattern valid
                    # so can break out of the inner for loop
                    break

    return is_valid[pattern]


count = 0
for pattern in patterns:
    if can_form(pattern, towels):
        count += 1
print("Part 1: ", count)


# =====================================================
# PART 2
# =====================================================


def count_arrangements(pattern, towels):
    """
    Same as above but instead of tracking True/False, keep track of counts.
    At each step, check ALL towels for validity. The counts are accumulated
    along the way.
    """
    counts = {}
    for i in range(len(pattern) + 1):
        counts[pattern[:i]] = 0
    counts[""] = 1  # there is one way to form a pattern with no towels

    for subpattern in counts:
        for towel in towels:
            if subpattern.endswith(towel):
                previous_subpattern = subpattern.removesuffix(towel)
                # if the previous_subpattern was not valid, just adds 0
                counts[subpattern] += counts[previous_subpattern]

    return counts[pattern]


count = 0
for pattern in patterns:
    count += count_arrangements(pattern, towels)
print("Part 1: ", count)
