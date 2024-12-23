import numpy
import os
import math
import numpy as np

def parse_file(file_path):
    with open(os.path.join(file_path)) as f:
        lines = f.read().splitlines()
    return lines

def operations(secret_number):
    secret_number = (secret_number * 64) ^ secret_number
    secret_number = secret_number % 16777216

    secret_number = int(secret_number / 32) ^ secret_number
    secret_number = secret_number % 16777216

    secret_number = (secret_number * 2048) ^ secret_number
    secret_number = secret_number % 16777216

    return secret_number

def n_operations(secret_number, n):

    differences = []
    last_dig = []
    last_digit = secret_number % 10
    for i in range(n):
        last_dig.append(secret_number % 10)
        secret_number = operations(secret_number)
        differences.append(secret_number% 10 - last_digit)

        last_digit = secret_number % 10

    last_dig.append(secret_number % 10)

    return secret_number, differences, last_dig

def get_sequence(last_dig, differences):

    dict_sequences = {}
    for i, value in enumerate(last_dig):

        if i < 4:
            continue

        diff = differences[i-4:i]


        if tuple(diff) in dict_sequences:
            continue
        else:
            dict_sequences[tuple(diff)] = value

    return dict_sequences


if __name__ == "__main__":

    file_path = "input.txt"
    #file_path = "test.txt"
    lines = parse_file(file_path)


    total = 0


    sequences_dict_list =  []
    for price in lines:
        result, differences, last_dig = n_operations(int(price),2000)
        total += result

        a = get_sequence(last_dig, differences)
        sequences_dict_list.append(a)

    print("Part 1: ", total)

    unique_sequences = {key for d in sequences_dict_list for key in d.keys()}

    unique_sequences = list(unique_sequences)
    final_dict = {}
    max = 0
    for i in unique_sequences:
        total_values = 0
        for seq in sequences_dict_list:
            try:
                total_values += seq[i]
            except:
                continue
        if total_values > 0:
            final_dict[i] = total_values

            if total_values > max:
                max = total_values
                max_sequence = i

    print("Part 2: ", max)

