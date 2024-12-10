import os
import numpy as np
import queue


def parse_file(file_path):
    with open(os.path.join(file_path)) as f:
        lines = f.read().splitlines()
    return np.array([[char for char in l] for l in lines])


def move_through_trail(pos, moves):
    j, i = pos

    for move in moves:
        if move == "L":
            i -= 1
        elif move == "R":
            i += 1
        elif move == "U":
            j -= 1
        elif move == "D":
            j += 1

    return (j, i)


def find_end_trail(trail, pos, moves):
    j, i = move_through_trail(pos, moves)

    # check that we got to the end of the trail
    if trail[j][i] == "9":
        return (j, i), True
    else:
        return (j, i), False


def valid_move(trail, pos, moves):
    j, i = move_through_trail(pos, moves)
    if i < 0 or j < 0 or i >= trail.shape[1] or j >= trail.shape[0]:
        return False
    if trail[j][i] == ".":
        return False
    if int(trail[j][i]) - int(trail[pos[0]][pos[1]]) != len(moves):
        return False

    return True


if __name__ == "__main__":

    import time

    time_start1 = time.time()
    file_name = "input.txt"
    data = parse_file(file_name)

    positions = np.argwhere(data == "0")

    total_trailheads = []
    total_unique_trailheads = []

    for initial_pos in positions:
        q = queue.Queue()
        path = ""
        q.put(path)

        unique_positions = []
        all_positions = []
        while True:
            # no more directions to check
            if q.empty():
                break
            path = q.get()

            # check if we have found the exit
            pos, found = find_end_trail(data, initial_pos, path)

            if found:
                if pos not in unique_positions:
                    unique_positions.append(pos)
                all_positions.append(pos)

            # add directions to the path and check if they are validß
            for next_step in ["L", "R", "U", "D"]:
                updated_path = path + next_step

                # check if the new path is valid
                if valid_move(data, initial_pos, updated_path):
                    q.put(updated_path)

        total_trailheads.append(all_positions)
        total_unique_trailheads.append(unique_positions)

    total_unique_sum = sum([len(i) for i in total_unique_trailheads])
    print("Total unique sum ", total_unique_sum)

    total_sum = sum([len(i) for i in total_trailheads])
    print("Total sum ", total_sum)

    print("Time taken: ", time.time() - time_start1)
