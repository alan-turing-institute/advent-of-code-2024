import re
import copy

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


def swap_numbers(input_sequence, num1, num2):
    output_sequence = copy.deepcopy(input_sequence)
    index1 = input_sequence.index(num1)
    index2 = input_sequence.index(num2)
    output_sequence[index1] = num2
    output_sequence[index2] = num1
    return output_sequence

def fix_sequence(sequence, rules):
    # find all the rules that apply to this sequence
    relevant_rules = [rule for rule in rules if (rule[0] in sequence) and (rule[1] in sequence)]
    # iteratively swap pairs that are in the wrong order
    solved = False
    while not solved:
        solved = True
        for rule in relevant_rules:
            if sequence.index(rule[0]) > sequence.index(rule[1]):
                solved = False
                sequence = swap_numbers(sequence, rule[0], rule[1])
    return sequence


def find_middle_page(sequence):
    return sequence[len(sequence)//2]

updates, rules = parse_input()
total = 0
incorrect_updates = []
for update in updates:
    for rule in rules:
        if not ((rule[0] in update) and (rule[1] in update)):
            continue
        if update.index(rule[0]) > update.index(rule[1]):
            incorrect_updates.append(update)
            break
for update in incorrect_updates:
    fixed_update = fix_sequence(update, rules)
    total += find_middle_page(fixed_update)


print(f"part 2: {total}")
