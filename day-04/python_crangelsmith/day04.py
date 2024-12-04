import os
import numpy as np


def parse_file(file_path):
    with open(os.path.join(file_path)) as f:
        lines = f.read().splitlines()
    return np.array([[char for char in l] for l in lines])


def count(data, string, reverse=False):
    word = list(string)

    if reverse:
        word = word[::-1]

    count_h = 0
    for (j, row) in enumerate(data):
        for (i, value) in enumerate(row):
            if value == word[0] and i + (len(word) - 1) < len(row):

                match = True
                for letter in range(1, len(word)):
                    if row[i + letter] != word[letter]:
                        match = False
                        break
                if not match:
                    continue

                count_h += 1
            else:
                continue
    return count_h

if __name__ == "__main__":

    # file_name = "test.txt"
    file_name = "input_day4.txt"

    data = parse_file(file_name)
    diagonals = ([np.diag(data, i).tolist() for i in range(-data.shape[0] + 1, data.shape[0])][::-1])

    data_T = data.T

    data_flip = np.fliplr(data)
    diagonals_flip = (
    [np.diag(data_flip, i).tolist() for i in range(-data_flip.shape[0] + 1, data_flip.shape[0])][::-1])

    # horizontal
    count_h = count(data, 'XMAS')
    count_h_r = count(data, 'XMAS', reverse=True)

    #vertical
    count_v = count(data_T, 'XMAS')
    count_v_r = count(data_T, 'XMAS', reverse=True)

    # diagonals
    count_d = count(diagonals, 'XMAS')
    count_d_r = count(diagonals, 'XMAS', reverse=True)

    # diagonals mirrored
    count_d_F = count(diagonals_flip, 'XMAS')
    count_d_F_r = count(diagonals_flip, 'XMAS', reverse=True)

    print("Solution for Part 1:",count_h + count_v + count_h_r + count_v_r + count_d + count_d_r + count_d_F + count_d_F_r)

    ### Part2
    indexes = index = np.where(data == "A")
    count_x = 0

    for i in range(0, len(indexes[0])):
        # check if the index is at the edge of the array
        if indexes[0][i] == 0 or indexes[1][i] == 0:
            continue
        elif indexes[0][i] == len(data) - 1 or indexes[1][i] == len(data) - 1:
            continue
        else:
            X1 = data[indexes[0][i] - 1, indexes[1][i] - 1] + data[indexes[0][i], indexes[1][i]] + data[
                indexes[0][i] + 1, indexes[1][i] + 1]
            X2 = data[indexes[0][i] + 1, indexes[1][i] - 1] + data[indexes[0][i], indexes[1][i]] + data[
                indexes[0][i] - 1, indexes[1][i] + 1]

            if (X1 in ['SAM', 'MAS']) and (X2 in ['SAM', 'MAS']):
                count_x += 1

    print("Solution for Part 2:", count_x)
