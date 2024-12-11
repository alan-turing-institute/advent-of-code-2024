import os
import math
from collections import defaultdict


def parse_file(file_path, delimiter=" "):
    with open(os.path.join(file_path)) as f:
        lines = f.read().splitlines()
    return [list(map(int, l.split(delimiter))) for l in lines][0]


def rules(value, count, temp):
    if value == 0:
        temp[1] += count
    else:
        log_val = int(math.log10(value) + 1)
        if (log_val % 2) == 0:
            first_half = value // 10 ** (log_val // 2)
            second_half = value % 10 ** (log_val // 2)
            temp[first_half] += count
            temp[second_half] += count
        else:
            temp[value * 2024] += count

    return temp



def blink_n_times(d_temp, n):
    output = defaultdict(int)
    for value, count in d_temp.items():
        output = rules(value, count, output)
    d_temp = output.copy()

    n = n - 1

    if n == 0:
        return d_temp
    else:
        return blink_n_times(d_temp, n)






if __name__ == "__main__":

    import time

    time_start1 = time.time()
    file_name = "input.txt"

    data = parse_file(file_name)


    n = 75
    total = 0
    for i in sorted(data):
        temp_i = defaultdict(int)
        temp_i[i] += 1
        temp_i  = blink_n_times(temp_i, n)

        for c in temp_i.values():
            total += c

    print("Part 2: ", total)


