import os
import numpy as np
import time


def parse_file(file_path, delimiter=" "):
    with open(os.path.join(file_path)) as f:
        lines = f.read().splitlines()
    return [list(map(int, l.split(delimiter))) for l in lines]


def get_order(order, initial_list):
    ordered_list = initial_list
    for i in initial_list:
        indexes = np.where(order == i)[0]
        sub_order = np.take(order, indexes, 0)

        for j in sub_order:
            index1 = np.where(ordered_list == j[0])[0]
            index2 = np.where(ordered_list == j[1])[0]

            # skip if either of the elements are not in the list or are ordered correctly
            if index1.size == 0 or index2.size == 0 or index1[0] < index2[0]:
                continue

            # delete element out of order and insert it before the element that should be after in the rule
            ordered_list = np.delete(ordered_list, index1)
            ordered_list = np.insert(ordered_list, index2[0], j[0])

    return ordered_list


def get_middle(arr):
    n = arr.shape[0] / 2.0
    n_int = int(n)
    return arr[n_int]


if __name__ == "__main__":

    time_start1 = time.time()
    file_name = "input_day5.txt"
    order_name = "input_printing.txt"
    # file_name = "Testday05.txt"
    # order_name = "testorderday05.txt"

    data = parse_file(file_name, delimiter="|")
    pages = parse_file(order_name, delimiter=",")

    final_correct_pages = []
    final_corrected_pages = []
    for page in pages:
        page = np.array(page)
        output_list = get_order(data, page)
        if np.all(page == output_list):
            final_correct_pages.append(get_middle(page))
        else:
            final_corrected_pages.append(get_middle(output_list))

    print("Solution part 1:", sum(final_correct_pages))
    print("Solution part 2:", sum(final_corrected_pages))
