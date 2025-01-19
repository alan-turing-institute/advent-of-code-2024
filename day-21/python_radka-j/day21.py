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
    Want to know: if the robot arm is currently above some "source" button, what buttons
    does the controlling arm above it have to use to get it to press the "target" button.

    Returns all _shortest_ paths between the source and target characters on the keypad
    using depth first search.

    The input here are POSITIONS of the source and target on the keypad, but we return
    the paths as a sequence of directional characters ("<>v^") followed by "A".

    For example, to get from A->5 on the numeric keypad retuns: ['<^^A', '^<^A', '^^<A']
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


def input_sequence(sequence, depth=0, n_directional_keypads=3):
    """
    Returns number of button presses required to input the given sequence of characters
    using the provided number of directional keypads:
    - start at the numeric keypad (depth=0) and move up as many directional keypads as
      have (the last directional keypad is operated by the human arm)
    - for each of the shortest paths between 2 characters in the sequence (i.e., buttons
      on the keypad), get the number of button presses required on the keyboard above it
      to move the arm between that sequence and recurse up to find the mininum required
    - cache shortest moves between character sequences at each depth as go along (part 2)
    """

    if (sequence, depth) in cache:
        return cache[(sequence, depth)]

    # last depth is a human arm --> just type in the given sequence (each char = 1 move)
    if depth == n_directional_keypads:
        return len(sequence)

    # only the first keypad is numeric, all other are directional
    if depth == 0:
        keypad = numeric_keypad
    else:
        keypad = directional_keypad

    # keypads are defined as {pos: char} but want to also access {char: pos}
    inv_keypad = {v: k for k, v in keypad.items()}

    # robot arm always starts above the A button
    source_pos = inv_keypad["A"]

    total_button_presses = 0
    for char in sequence:
        target_pos = inv_keypad[char]

        shortest_paths = get_shortest_paths(source_pos, target_pos, keypad)
        count_path_button_presses = [
            input_sequence(path, depth + 1, n_directional_keypads)
            for path in shortest_paths
        ]
        total_button_presses += min(count_path_button_presses)
        source_pos = target_pos

    cache[(sequence, depth)] = total_button_presses
    return total_button_presses


def calculate_score(codes, n_directional_keypads=3):
    tot_sum = 0
    for code in codes:
        score = input_sequence(code, n_directional_keypads=n_directional_keypads)
        tot_sum += score * int(code[:-1])
    return tot_sum


# codes = ["029A", "980A", "179A", "456A", "379A"]
codes = ["140A", "143A", "349A", "582A", "964A"]

# PART 1
cache = {}
print("part 1:", calculate_score(codes))

# PART 2
cache = {}
print("part 1:", calculate_score(codes, n_directional_keypads=26))
