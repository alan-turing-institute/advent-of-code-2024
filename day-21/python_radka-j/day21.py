# DIRECTIONAL KEYPAD
#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+

directional_keypad = {(0, 1): "^", (0, 2): "A", (1, 0): "<", (1, 1): "v", (1, 2): ">"}

# NUMERIC KEYPYAD
# +---+---+---+
# | 7 | 8 | 9 |
# +---+---+---+
# | 4 | 5 | 6 |
# +---+---+---+
# | 1 | 2 | 3 |
# +---+---+---+
#     | 0 | A |
#     +---+---+

numeric_keypad = {
    (0, 0): "7",
    (0, 1): "8",
    (0, 2): "9",
    (1, 0): "4",
    (1, 1): "5",
    (1, 2): "6",
    (2, 0): "1",
    (2, 1): "2",
    (2, 2): "3",
    (3, 1): "0",
    (3, 2): "A",
}


def get_neighbours(pos, keypad):
    """
    Given a position on the keypad, return adjacent positions and the direction one
    needs to take to get there (i.e., one of "<>v^").
    """
    valid = []
    moves = {(-1, 0): "^", (0, -1): "<", (1, 0): "v", (0, 1): ">"}
    for direction in moves:
        new_pos = (pos[0] + direction[0], pos[1] + direction[1])
        if new_pos in keypad:
            valid.append((new_pos, moves[direction]))
    return valid


def get_shortest_paths(source_pos, target_pos, keypad):
    """
    Want to know: if the robot arm is currently above some "source" button -> what moves
    does the controlling arm have to make to get it to press the "target" button.

    Returns all _shortest_ paths between the source and target characters on the keypad.

    The input here are POSITIONS of the source and target on the keypad, but we return
    the paths as a sequence of directional characters ("<>v^") followed by "A".
    """
    # get ALL paths
    paths = []
    # keep track of visited positions to avoid looping
    stack = [(source_pos, "", [])]
    min_len = float("inf")
    while stack:
        curr_pos, path, visited = stack.pop()
        if curr_pos == target_pos:
            # always end the path with the "A" key to press the button at target_pos
            paths.append(path + "A")
            if len(paths[-1]) < min_len:
                min_len = len(paths[-1])
        for neighbour_pos, direction in get_neighbours(curr_pos, keypad):
            if neighbour_pos not in visited:
                stack.append((neighbour_pos, path + direction, visited + [curr_pos]))

    # have all paths, now only return the shortest paths
    return [path for path in paths if len(path) == min_len]


cache = {}


def input_code(code, keypads, level=0):
    """
    Returns number of button presses required to input the given code using the provided
    number of keypads:
    - start at the numeric keypad (level=0) and move up as many keypads as have
    - for each of the shortest paths between 2 buttons, get the number of button presses
      required on the keyboard above it to move the arm between them and pick the minimum
    - cache best moves at each level as go along
    """
    if (code, level) in cache:
        return cache[(code, level)]

    # last level is a human arm --> just type in the given sequence (each char = 1 move)
    if level == len(keypads):
        return len(code)

    # keypads are defined as {pos: char} but want to also access {char: pos}
    keypad = keypads[level]
    inv_keypad = {v: k for k, v in keypad.items()}

    # robot arm always starts above the A button
    source_pos = inv_keypad["A"]

    total_button_presses = 0
    for char in code:
        target_pos = inv_keypad[char]

        shortest_paths = get_shortest_paths(source_pos, target_pos, keypad)
        count_path_button_presses = [
            input_code(path, keypads, level + 1) for path in shortest_paths
        ]
        total_button_presses += min(count_path_button_presses)
        source_pos = target_pos

    cache[(code, level)] = total_button_presses
    return total_button_presses


def calculate_score(codes, keypads):
    tot_sum = 0
    for code in codes:
        score = input_code(code, keypads)
        tot_sum += score * int(code[:-1])
    return tot_sum


codes = ["140A", "143A", "349A", "582A", "964A"]
# codes = ["029A", "980A", "179A", "456A", "379A"]

# PART 1
cache = {}
keypads = [numeric_keypad, directional_keypad, directional_keypad]
print("part 1:", calculate_score(codes, keypads))

# PART 2
cache = {}
keypads2 = [numeric_keypad] + [directional_keypad] * 25
print("part 1:", calculate_score(codes, keypads2))
