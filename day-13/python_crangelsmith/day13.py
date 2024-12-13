import numpy
import os
import math


def parse_file(file_path):
    with open(os.path.join(file_path)) as f:
        lines = f.read().splitlines()
    return lines


def get_cost(solution, limit=None):
    if solution[0] < 0 or solution[1] < 0:
        return 0

    if limit:
        if solution[0] > limit or solution[1] > limit:
            return 0

    is_integer1 = round(round(solution[0], 4) - round(solution[0], 0), 2) == 0
    is_integer2 = round(round(solution[1], 4) - round(solution[1], 0), 2) == 0

    if not is_integer1 or not is_integer2:
        return 0

    cost = round(solution[0] * 3 + solution[1])
    return cost


if __name__ == "__main__":

    file_name = "input.txt"
    # file_name = "test.txt"

    data = parse_file(file_name)

    wins_part1 = []
    wins_part2 = []

    for index, row in enumerate(data):

        line_A = row.split(", ")

        if "A" not in line_A[0]:
            continue

        A_eq1 = int(line_A[0][12:])
        A_eq2 = int(line_A[1][2:])

        line_B = data[index + 1].split(", ")
        B_eq1 = int(line_B[0][12:])
        B_eq2 = int(line_B[1][2:])

        sol = data[index + 2].split(",")

        sol_eq1 = int(sol[0][9:])
        sol_eq2 = int(sol[1][3:])

        shift = int(10000000000000)

        a = [[A_eq1, B_eq1], [A_eq2, B_eq2]]
        b_part1 = [sol_eq1, sol_eq2]
        solution_1 = numpy.linalg.lstsq(a, b_part1)[0]

        b_part2 = [sol_eq1 + shift, sol_eq2 + shift]
        solution_2 = numpy.linalg.lstsq(a, b_part2)[0]

        cost1 = get_cost(solution_1, limit=100)
        cost2 = get_cost(solution_2)

        max_cost = 400
        if max_cost > cost1 > 0:
            wins_part1.append(cost1)

        if cost2 > 0:
            wins_part2.append(cost2)

    print("Solution part 1: ", sum(wins_part1))
    print("Solution part 2: ", sum(wins_part2))
