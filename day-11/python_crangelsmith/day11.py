import os
import math
from collections import defaultdict


def parse_file(file_path, delimiter=" "):
    with open(os.path.join(file_path)) as f:
        lines = f.read().splitlines()
    return [list(map(int, l.split(delimiter))) for l in lines][0]


def rules(value, count, data_dict):
    if value == 0:
        data_dict[1] += count
    else:
        log_val = int(math.log10(value) + 1)
        if (log_val % 2) == 0:
            first_half = value // 10 ** (log_val // 2)
            second_half = value % 10 ** (log_val // 2)
            data_dict[first_half] += count
            data_dict[second_half] += count
        else:
            data_dict[value * 2024] += count

    return data_dict


def blink_n_times(data, n):
    output = defaultdict(int)
    for value, count in data.items():
        output = rules(value, count, output)
    data = output.copy()

    n = n - 1

    if n == 0:
        return data
    else:
        return blink_n_times(data, n)


if __name__ == "__main__":

    file_name = "input.txt"
    data = parse_file(file_name)

    n = 75
    total = 0
    for i in sorted(data):
        result_i = defaultdict(int)
        result_i[i] += 1
        result_i = blink_n_times(result_i, n)

        for value in result_i.values():
            total += value

    print("Part 2: ", total)
