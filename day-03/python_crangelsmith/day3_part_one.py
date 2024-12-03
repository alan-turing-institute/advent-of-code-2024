import os
from operator import mul
import re


def parse_file(file_path: str) -> list[list[int]]:
    with open(os.path.join(file_path)) as f:
        lines = f.read()
    return lines


def evaluate_matches(matches):
    do_operation = True
    sum_total = 0

    for i in matches:
        if i.startswith("mul") and do_operation:
            sum_total += eval(i)
        elif i == "don't()":
            do_operation = False
        elif i == "do()":
            do_operation = True
    return sum_total


if __name__ == "__main__":

    file_name = "input_day3.txt"
    data = parse_file(file_name)

    regex1 = r"mul\([\d]+,[\d]+\)"
    values = [eval(i) for i in re.findall(regex1, data)]

    print("Solution part 1", sum(values))

    regex2 = r"mul\([\d]+,[\d]+\)|do\(\)|don't\(\)"
    matches = re.findall(regex2, data)

    print("Solution part 2:", evaluate_matches(matches))





