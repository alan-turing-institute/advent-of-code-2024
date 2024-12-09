import os
import numpy as np

import itertools


def parse_file(file_path):
    with open(os.path.join(file_path)) as f:
        return f.read().replace('\n', '')


def expand(data, spaces, index, output):

    for i in range(0,int(data)):
        output.append(str(index))

    for i in range(0,int(spaces)):
        output.append(".")
    return output

def strictly_increasing_by_one(L):
    return all(y-x==1 for x, y in zip(L, L[1:]))

if __name__ == "__main__":

    import time

    time_start1 = time.time()
    data = "2333133121414131402"
    file_name = "input.txt"
    # data = "12345"

    data = parse_file(file_name)
    #data = "12345"


    count = 0
    output = []

    for i in range(0, len(data), 2):
        file = data[i]

        if i + 1 < len(data):
            spaces = data[i + 1]
        else:
            spaces = "0"

        output = expand(file, spaces, str(count), output)
        count += 1

    old_output = output
    indexes = [i for i, x in enumerate(output) if x == "."]


    count = 0
    while True:

        i = output[-1]

        count += 1
        if i == ".":
            output = output[:-1]
        else:
            output = output[: indexes[0]] + [i] + output[indexes[0] + 1:-1]
            indexes.pop(0)

        if not "." in output:
            break


    checksum = 0
    for i, value in enumerate(output):
        if value == ".":
            continue
        checksum += i * int(value)

    print("Checksum: ", checksum)
    time_end1 = time.time()
    print("Time taken: ", time_end1 - time_start1)


