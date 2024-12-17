import os
import numpy as np


def parse_file_grid(file_path):
    with open(os.path.join(file_path)) as f:
        lines = f.read().splitlines()
    return np.array([[char for char in l] for l in lines])

def parse_file_moves(file_path):
    with open(os.path.join(file_path)) as f:
        return f.read().replace('\n', '')


# function to perform the task

def shift_sublist_left(test_list, strt_idx, no_ele, shft_idx):
    # Extract the sublist to be moved
    sublist = [test_list[strt_idx]]

    replacing_list = test_list[strt_idx+1:shft_idx+no_ele]

    # Remove the sublist from its original position
    remaining_list = test_list[:strt_idx]

    # Insert the sublist into its new position
    return remaining_list + replacing_list + sublist


def shift_sublist_right(test_list, space_idx, no_ele, robot_idx):
    # Extract the sublist to be moved
    sublist =  [test_list[space_idx]]

    replacing_list = test_list[robot_idx:robot_idx + no_ele]

    # Remove the sublist from its original position
    remaining_list = test_list[space_idx+1:]

    # Insert the sublist into its new position
    return sublist + replacing_list + remaining_list


def move_robots(l, index, move):
    if move == "<" or move == "^":
        subl = l[:index + 1]
        robot_pos = np.argwhere(subl == "@").flatten()[-1]
        if "#" in subl:
            index_wall = np.argwhere(subl == "#").flatten()
        if "." in subl:
            index_space = np.argwhere(subl == ".").flatten()
        else:
            return l

        if index_wall.max() < index_space.max():
            subl = shift_sublist_left(list(subl), index_space.max(), robot_pos - index_space.max(), robot_pos)
            l = subl + list(l[index + 1:])

    if move == ">" or move == "v":
        subl = l[index:]
        robot_pos = np.argwhere(subl == "@").flatten()[-1]
        if "#" in subl:
            index_wall = np.argwhere(subl == "#").flatten()
        if "." in subl:
            index_space = np.argwhere(subl == ".").flatten()
        else:
            return l
        if index_wall.min() > index_space.min():
            subl = shift_sublist_right(list(subl), index_space.min(), index_space.min() - robot_pos, robot_pos)
            l = list(l[:index]) + subl

    return l
if __name__ == "__main__":

    import time

    time_start1 = time.time()
    file_name = "input.txt"
    #file_name = "test1.txt"
    moves_name = "moves.txt"

    data = parse_file_grid(file_name)
    moves = parse_file_moves(moves_name)


    for move in moves:
        pos_y, pos_x = np.argwhere(data == "@")[0]

        if move=="<" or move==">":
            index = pos_x
            l = data[pos_y, :]

            data[pos_y, :] = move_robots(l, index, move)

        if move=="^" or move=="v":
            index = pos_y
            l = data[:, pos_x]
            data[:, pos_x] = move_robots(l, index, move)

        print("Move", move)
        print(data)

    postions = np.argwhere(data == "O")

    total = 0
    for i in range(0,len(postions)):
        pos_0_y, pos_0_x = postions[i]
        total+= (100*pos_0_y) + pos_0_x

    print("Part1: total", total)

