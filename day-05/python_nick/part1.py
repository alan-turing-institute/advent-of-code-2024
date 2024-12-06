import re

def parse_input():
    inputlines = open("input.txt", "r").readlines()
    rules = []
    updates = []
    for line in inputlines:
        rule_search = re.search("([\d]+)\|([\d]+)", line)
        if rule_search:
            rules.append((int(rule_search.groups()[0]), int(rule_search.groups()[1])))
        update_search = re.search("([\d]+,)+", line)
        if update_search:
            pages = [int(page) for page in line.split(",")]
            updates.append(pages)
    return updates, rules

def apply_rules(sequence, rules):
    """
    return False if a sequence (list of numbers) violates a rule (tuple of two numbers)
    """
    for rule in rules:
        if not ((rule[0] in sequence) and (rule[1] in sequence)):
            continue
        if sequence.index(rule[0]) > sequence.index(rule[1]):
            return False
    return True

def find_middle_page(sequence):
    return sequence[len(sequence)//2]

updates, rules = parse_input()
total = 0
for update in updates:
    if apply_rules(update, rules):
        total += find_middle_page(update)


print(f"part 1: {total}")
