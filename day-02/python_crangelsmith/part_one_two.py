import os


def parse_file(file_path):
    with open(os.path.join(file_path)) as f:
        lines = f.read().splitlines()
    return [list(map(int, l.split(" "))) for l in lines]


def check_condition(input_list):
    if input_list != sorted(input_list) and input_list != sorted(input_list, reverse=True):
        return False

    for i, l in enumerate(input_list[:-1]):
        diff = abs(l - input_list[i + 1])
        if diff < 1 or diff > 3:
            return False
    # If we get here, the list is sorted and the differences are all within 1-3
    return True


def drop_level_check(input_list):
    for i in range(0, len(input_list)):
        new_list = [l for j, l in enumerate(input_list) if j != i]
        if check_condition(new_list):
            return True

    # If we get here, we couldn't find a valid list by dropping one element
    return False


if __name__ == "__main__":
    data = parse_file('input.txt')

    # part 1
    report_count = 0
    for report in data:
        if check_condition(report):
            report_count += 1

    print("Solution to Part 1 ", report_count)

    # part 2
    report_count_2 = 0
    for report in data:
        if check_condition(report):
            report_count_2 += 1
        elif drop_level_check(report):
            report_count_2 += 1
    print("Solution to Part 2 ", report_count_2)
