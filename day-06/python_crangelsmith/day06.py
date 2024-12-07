import os
import numpy as np


def parse_file(file_path):
    with open(os.path.join(file_path)) as f:
        lines = f.read().splitlines()
    return np.array([[char for char in l] for l in lines])


def find_exit(input_data, indexes,max_repeats=100):
    data = input_data.copy()
    infite_loop = False

    count_rotations = 0
    count_repeat = 0
    while True:
        if data[indexes] == "N":
            break
        if data[indexes[0] - 1, indexes[1]] != "#":
            if data[indexes] == "X" or data[indexes] == "H":
                data[indexes] = "H"
            else:
                data[indexes] = "X"
            if data[indexes] == "H" and data[indexes[0] - 1, indexes[1]] == "H" and previous == "H":
                count_repeat += 1
                if count_repeat > max_repeats:
                    infite_loop = True
                    break
            previous = data[indexes]
            indexes = (indexes[0] - 1, indexes[1])

        else:
            value_before = data[indexes]
            data[indexes] = "R"
            data = np.rot90(data, axes=(0, 1))
            indexes = np.where(data == "R")
            data[indexes] = value_before
            count_rotations += 1

    while True:
        data = np.rot90(data, axes=(1, 0))
        if data[(0, 0)] == "1":
            break

    data[np.where(data == "H")] = "X"

    if infite_loop:
        return -1, data
    else:
        return len(np.where((data == "X"))[0]), data

if __name__ == "__main__":

    import time

    time_start1 = time.time()
    file_name = "test.txt"
    file_name = "input_day6.txt"

    data = parse_file(file_name)

    data = np.pad(data, 1, mode='constant', constant_values='N')
    data[(0, 0)] = 1

    indexes = np.where(data == "^")

    solution, path_data = find_exit(data, indexes)

    print("Solution for Part 1:", solution)

    # Part 2

    time_start1 = time.time()
    x, y = np.where(path_data == "X")

    count_infinite = 0
    for i in range(0, len(x)):
        if indexes == (x[i], y[i]):
            continue
        new_data = data.copy()
        new_data[x[i], y[i]] = "#"
        solution, path_data = find_exit(new_data, indexes,50)

        if solution == -1:
            count_infinite += 1
            print(i, "Infinite loop found")

    time_start2 = time.time()

    print("Solution for Part 2:", count_infinite)
    print("Time for Part 2:", time_start2 - time_start1)
