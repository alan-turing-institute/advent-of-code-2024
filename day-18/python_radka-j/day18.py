import numpy as np

with open("input.txt") as f:
    lines = f.read().splitlines()


def get_shortest_path(bytes_size):
    # grid with coordinates 0-70 in both directions
    grid = [["."] * 71 for _ in range(71)]

    # fill up space for the given number of bytes steps
    for i in range(bytes_size):
        col, row = [int(val) for val in lines[i].split(",")]
        grid[row][col] = "#"

    # construct queue
    queue = {}
    for i in range(71):
        for j in range(71):
            queue[(i, j)] = np.inf

    start = (0, 0)
    queue[start] = 0
    end = (70, 70)

    # get shortest path from start to end
    while queue:

        # get the next node with currently shortest distance to start
        curr_pos = min(queue, key=queue.get)
        curr_score = queue[curr_pos]

        # if only infinite distance nodes remain in queue - they are unreachable
        # so the path to the end has been blocked
        if curr_score == np.inf:
            return "BLOCKED"

        # shortest path to end
        if curr_pos == end:
            return curr_score

        for direction in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
            new_pos = (curr_pos[0] + direction[0], curr_pos[1] + direction[1])
            # if new_pos isn't in the queue it's outside the range or already been visited
            if new_pos in queue:
                if grid[new_pos[0]][new_pos[1]] != "#":
                    queue[new_pos] = min(queue[new_pos], curr_score + 1)

        # remove current node from queue (the univisited set)
        del queue[curr_pos]


print("Part 1: ", get_shortest_path(1024))

# PART 2
# use binary search to try byte size values between 1024 and lenght of list
# find the first byte at which the path is blocked
start_val = 0
end_val = 3450

lowest_blocked_byte = end_val + 1

while start_val <= end_val:
    b = (end_val + start_val) // 2
    res = get_shortest_path(b)
    if res == "BLOCKED":
        if b < lowest_blocked_byte:
            lowest_blocked_byte = b
        end_val = b - 1
    else:
        start_val = b + 1

# return the positio of the last byte that blocked the path
print("Part 2: ", lines[lowest_blocked_byte - 1])
