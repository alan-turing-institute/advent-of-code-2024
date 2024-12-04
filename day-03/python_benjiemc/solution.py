import re
import sys


def part1(contents):
    valid = re.findall(r'mul\(([0-9]+),([0-9]+)\)', contents)
    return sum([int(x1) * int(x2) for x1, x2 in valid])


def part2(contents):
    instructions = re.findall(r"mul\([0-9]+,[0-9]+\)|do\(\)|don't\(\)", contents)

    total = 0
    active = True
    for instruction in instructions:
        if instruction == 'do()' and not active:
            active = True

        elif instruction == "don't()" and active:
            active = False

        if instruction.startswith('mul(') and active:
            match = re.match(r'mul\(([0-9]+),([0-9]+)\)', instruction)
            total += int(match.group(1)) * int(match.group(2))

    return total


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as fh:
        contents = fh.read()

    print('Part 1 solution:', part1(contents))
    print('Part 2 solution:', part2(contents))
