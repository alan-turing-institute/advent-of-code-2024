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
            elif char == "[":
                boxes.add((r, c))
    return robot_pos, boxes


def scale_up_warehouse(warehouse):
    scaled_warehouse = []
    for row in warehouse:
        scaled_row = ""
        for char in row:
            if char == "#":
                scaled_row += "##"
            elif char == "O":
                scaled_row += "[]"
            elif char == ".":
                scaled_row += ".."
            elif char == "@":
                scaled_row += "@."
        scaled_warehouse.append(scaled_row)
    return scaled_warehouse


def simulate_robot_moves(warehouse, moves):
    directions = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}
    warehouse = [list(row) for row in warehouse]
    robot_pos, boxes = find_robot_position_and_boxes(warehouse)

    for move in moves:
        dr, dc = directions[move]
        new_robot_pos = (robot_pos[0] + dr, robot_pos[1] + dc)

        # Check if robot's new position is blocked
        if warehouse[new_robot_pos[0]][new_robot_pos[1]] == "#":
            continue

        # Handle wide box movement
        if warehouse[new_robot_pos[0]][new_robot_pos[1]] in ("[", "]"):
            box_pos = new_robot_pos
            box_pair_pos = (
                (box_pos[0], box_pos[1] + 1)
                if dc != 0
                else (box_pos[0] + 1, box_pos[1])
            )

            # Ensure box_pos always refers to '[' if robot encounters ']'
            if warehouse[box_pos[0]][box_pos[1]] == "]":
                box_pos = (box_pos[0], box_pos[1] - 1)
                box_pair_pos = (
                    (box_pos[0], box_pos[1] + 1)
                    if dc != 0
                    else (box_pos[0] + 1, box_pos[1])
                )

            next_box_pos = (box_pos[0] + dr, box_pos[1] + dc)
            next_box_pair_pos = (box_pair_pos[0] + dr, box_pair_pos[1] + dc)

            # Check if the box can move
            if (
                warehouse[next_box_pos[0]][next_box_pos[1]] == "."
                and warehouse[next_box_pair_pos[0]][next_box_pair_pos[1]] == "."
            ):
                # Move the wide box
                warehouse[box_pos[0]][box_pos[1]] = "."
                warehouse[box_pair_pos[0]][box_pair_pos[1]] = "."
                warehouse[next_box_pos[0]][next_box_pos[1]] = "["
                warehouse[next_box_pair_pos[0]][next_box_pair_pos[1]] = "]"

                # Update box positions
                boxes.remove(box_pos)
                boxes.add(next_box_pos)

            else:
                continue  # Box cannot move, skip robot movement

        # Move the robot
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
        gps_sum += 100 * r + c // 2  # Adjust for scaled warehouse
    return gps_sum


def main():
    map_lines, moves = read_input("input.txt")
    scaled_warehouse = scale_up_warehouse(map_lines)
    final_boxes = simulate_robot_moves(scaled_warehouse, moves)
    gps_sum = calculate_gps_sum(final_boxes, scaled_warehouse)
    print(f"Sum of all boxes' GPS coordinates in scaled warehouse: {gps_sum}")


if __name__ == "__main__":
    main()
