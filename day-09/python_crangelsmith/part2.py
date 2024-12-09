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

    data = parse_file(file_name)

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


    indexes = [i for i, x in enumerate(output) if x == "."]

    count = 0
    last_index = 'X'
    for index, i in reversed(list(enumerate(output))):
        if i == '0':
            break
        if i == last_index:
            continue
        if i == ".":
            continue

        count_repeated = 1
        for j in reversed(output[:index]):
            if j == i:
                count_repeated += 1
            else:
                break

        # does indexes have count_repeated elements that are strictly increasing by one?
        first_index = -1
        for s in range(0, len(indexes)):
            sub_index = indexes[s:count_repeated + s]
            if strictly_increasing_by_one(sub_index) and len(sub_index) == count_repeated:
                first_index = s
                break

        if first_index == -1 or indexes[s] > index:
            last_index = i
            continue

        cr = 0
        for sub_index in indexes[first_index:count_repeated + first_index]:
            output = output[:sub_index] + [i] + output[sub_index + 1:]
            output = output[:index -cr] + ["."] + output[(index-cr) + 1:]

            cr += 1

            indexes.pop(s)
            last_index = i


    checksum = 0
    for i, value in enumerate(output):
        if value == ".":
            continue
        checksum += i * int(value)

    print("Checksum: ", checksum)
    time_end1 = time.time()
    print("Time taken: ", time_end1 - time_start1)


