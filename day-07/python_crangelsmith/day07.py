
import os
import numpy as np
import itertools


def parse_file(file_path):
    with open(os.path.join(file_path)) as f:
        lines = f.read().splitlines()
    return lines

def get_combinations(list_combinations,operators):

    dict_combinations = {}
    for n in list_combinations:
        dict_combinations[n] = [''.join(p) for p in itertools.product(operators, repeat=n)]

    return dict_combinations

def operations(calibrations, combinations, reference_value):

    for comb in combinations:
        counter = 0
        result = calibrations[counter]

        for o in comb:
            if o == "|":
                result = int(str(result) + calibrations[counter + 1])
            else:
                if o == "+":
                    result = int(result) + int(calibrations[counter + 1])
                elif o == "*":
                    result = int(result) * int(calibrations[counter + 1])
                #result = eval(str(result) + o + calibrations[counter + 1])
            counter += 1

        if reference_value == result:
            print("Found it", comb, result)
            return result

    return 0




if __name__ == "__main__":

    import time

    time_start1 = time.time()
    file_name = "test.txt"
    file_name = "input_day7.txt"

    data = parse_file(file_name)
    data = [i.split(":") for i in data]
    data = [[i[0], i[1].split(" ")[1:]] for i in data]

    n_combinations = np.unique([len(data[i][1])-1 for i in range(0, len(data))])

    possible_combinations_part1 = get_combinations(n_combinations, "+*")
    possible_combinations_part2 = get_combinations(n_combinations, "+*|")



    correct_part1 = []
    correct_part2 = []

    for example in data:

        total = int(example[0])
        calibrations = example[1]

        n = len(calibrations)-1
        # part 1

        combinations_part1 = possible_combinations_part1[n]
        correct_part1.append(operations(calibrations, combinations_part1,total))

        # part 2
        combinations_part2 = possible_combinations_part2[n]
        correct_part2.append(operations(calibrations, combinations_part2,total))


    print("Solution to Part 1 ", sum(correct_part1))
    print("Solution to Part 2 ", sum(correct_part2))

    time_start2 = time.time()
    print("Time taken", time_start2 - time_start1)
