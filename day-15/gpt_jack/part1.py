def read_input(file_name):
    with open(file_name, "r") as f:
        lines = f.read().splitlines()

    # Separate the map and moves
    map_lines = []
    moves = []
    for line in lines:
        if line.startswith("#") or "@" in line:
            map_lines.append(line)
        elif any(c in line for c in "^v<>"):
            moves.append(line.strip())

    # Combine moves into a single string
    moves = "".join(moves)
    return map_lines, moves


def find_robot_position_and_boxes(warehouse):
    robot_pos = None
    boxes = set()
    for r, row in enumerate(warehouse):
        for c, char in enumerate(row):
            if char == "@":
                robot_pos = (r, c)
            elif char == "O":
                boxes.add((r, c))
    return robot_pos, boxes


def simulate_robot_moves(warehouse, moves):
    directions = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}
    warehouse = [list(row) for row in warehouse]
    robot_pos, boxes = find_robot_position_and_boxes(warehouse)

    for move in moves:
        dr, dc = directions[move]
        new_robot_pos = (robot_pos[0] + dr, robot_pos[1] + dc)

        # Check the new position
        if warehouse[new_robot_pos[0]][new_robot_pos[1]] == "#":
            continue  # Wall, skip move

        # Handle pushing multiple boxes
        current_pos = new_robot_pos
        chain_positions = []
        while current_pos in boxes:
            next_pos = (current_pos[0] + dr, current_pos[1] + dc)
            if warehouse[next_pos[0]][next_pos[1]] == "#":
                break  # Blocked by wall
            chain_positions.append(current_pos)
            current_pos = next_pos

        # If all boxes in the chain can move, move them
        if (
            len(chain_positions) > 0
            and warehouse[current_pos[0]][current_pos[1]] == "."
        ):
            for pos in reversed(chain_positions):
                next_pos = (pos[0] + dr, pos[1] + dc)
                boxes.remove(pos)
                boxes.add(next_pos)
                warehouse[next_pos[0]][next_pos[1]] = "O"
                warehouse[pos[0]][pos[1]] = "."

        # Move the robot
        if new_robot_pos not in boxes:
            warehouse[robot_pos[0]][robot_pos[1]] = "."
            warehouse[new_robot_pos[0]][new_robot_pos[1]] = "@"
            robot_pos = new_robot_pos

    # Debug: Print final state of the warehouse
    print("Final warehouse state:")
    for row in warehouse:
        print("".join(row))

    return boxes


def calculate_gps_sum(boxes, warehouse):
    gps_sum = 0
    for r, c in boxes:
        gps_sum += 100 * r + c
    return gps_sum


def main():
    map_lines, moves = read_input("input.txt")
    final_boxes = simulate_robot_moves(map_lines, moves)
    gps_sum = calculate_gps_sum(final_boxes, map_lines)
    print(f"Sum of all boxes' GPS coordinates: {gps_sum}")


if __name__ == "__main__":
    main()
