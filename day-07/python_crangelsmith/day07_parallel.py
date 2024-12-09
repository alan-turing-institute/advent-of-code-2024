
import os
import itertools
from multiprocessing import Pool, cpu_count


def parse_file(file_path):
    with open(os.path.join(file_path)) as f:
        lines = f.read().splitlines()
    return lines

def generate_combinations(n, operators):

    return [''.join(p) for p in itertools.product(operators, repeat=n)]


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

            counter += 1

        if int(reference_value) == int(result):
            return result

    return 0


def process_example(example, possible_combinations_part1, possible_combinations_part2):
    total = int(example[0])
    calibrations = example[1]
    n = len(calibrations) - 1

    # Part 1
    combinations_part1 = possible_combinations_part1[n]
    match = operations(calibrations, combinations_part1, total)
    correct_part1 = match

    # Part 2
    if match == 0:
        combinations_part2 = possible_combinations_part2[n]
        correct_part2 = operations(calibrations, combinations_part2, total)

    else:
        correct_part2 = correct_part1

    return correct_part1, correct_part2



if __name__ == "__main__":

    import time

    time_start1 = time.time()
    file_name = "test.txt"
    file_name = "input_day7.txt"

    data = parse_file(file_name)
    data = [i.split(":") for i in data]
    data = [[i[0], i[1].split(" ")[1:]] for i in data]

    n_combinations = set(len(item[1]) - 1 for item in data)
    possible_combinations_part1 = {n: generate_combinations(n, "+*") for n in n_combinations}
    possible_combinations_part2 = {
        n: [comb for comb in generate_combinations(n, "+*|") if "|" in comb]
        for n in n_combinations
    }

    # parallel processing
    with Pool(cpu_count()) as pool:
        results = pool.starmap(
            process_example,
            [(example, possible_combinations_part1, possible_combinations_part2) for example in data]
        )

    # get results from the parallel processing
    correct_part1 = sum(result[0] for result in results)
    correct_part2 = sum(result[1] for result in results)

    print("Solution to Part 1 ", correct_part1)
    print("Solution to Part 2 ", correct_part2)

    time_start2 = time.time()
    print("Time taken", time_start2 - time_start1)
