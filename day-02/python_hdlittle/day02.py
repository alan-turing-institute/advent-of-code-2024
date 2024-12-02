from itertools import pairwise
lims = (1, 3)
with open("input.txt") as file:
    lines = [line.strip().split(" ") for line in file]

# str to int
lines = [[int(level) for level in report] for report in lines]


def safe(input_list):
    """Checks if a list is safe returns True/False"""

    difference = [a-b for a, b in pairwise(input_list)]
    abs_difference = [abs(x) for x in difference]

    # The levels are either all increasing or all decreasing
    all_pos = all(diff > 0 for diff in difference)
    all_neg = all(diff < 0 for diff in difference)
    if not (all_neg or all_pos):
        return False

    # Any two adjacent levels differ by at least one and at most three
    if not ((max(abs_difference) <= lims[1]) and (min(abs_difference) >= lims[0])):
        return False
    
    return True


safe_reports = sum(1 for line in lines if safe(line))

print(f"Part 1 = {safe_reports}")


def prob_damp(input_list):
    """Can you get rid of one dodgy level returns True/False"""
    for i in range(len(input_list)):
        mod_list = input_list[:i] + input_list[i+1:]
        if safe(mod_list):
            return True
    return False


prob_safe = sum(1 for line in lines if not safe(line) and prob_damp(line))

print(f"Part 2 = {safe_reports + prob_safe}")
