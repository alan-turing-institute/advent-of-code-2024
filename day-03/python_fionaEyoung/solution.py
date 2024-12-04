import re
from functools import reduce

def main():
    fname = 'input.txt'

    with open(fname, 'r') as file:
        memory = file.read()

    num_pattern = '\d{1,3}'
    pattern = f'mul\({num_pattern},{num_pattern}\)'

    # Part 1

    matches = re.findall(pattern, memory)

    total = 0
    for op in matches:
        total += reduce(lambda x, y: x*y, [int(match) for match in re.findall(num_pattern, op)])

    print("Part 1: ", total)

    # Part 2

    parts = [chunk.split("do()") for chunk in memory.split("don't()")]

    total = 0
    for chunk in memory.split("do()"):
        do_chunk = chunk.split("don't()", maxsplit=1)[0]
        matches = re.findall(pattern, do_chunk)
        for op in matches:
            total += reduce(lambda x, y: x*y, [int(match) for match in re.findall(num_pattern, op)])

    print("Part 2: ", total)

if __name__=='__main__':
    main()
