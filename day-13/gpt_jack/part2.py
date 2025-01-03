def parse_input(file_path):
    machines = []
    with open(file_path, "r") as file:
        lines = [
            line.strip() for line in file if line.strip()
        ]  # Strip lines and skip empty ones
        for i in range(0, len(lines), 3):
            button_a = lines[i].split(",")
            button_b = lines[i + 1].split(",")
            prize = lines[i + 2].split(",")

            a_x = int(button_a[0].split("+")[1])  # Extract X value after 'X+'
            a_y = int(button_a[1].split("+")[1])  # Extract Y value after 'Y+'
            b_x = int(button_b[0].split("+")[1])
            b_y = int(button_b[1].split("+")[1])
            p_x = int(prize[0].split("=")[1]) + 10000000000000  # Corrected X value
            p_y = int(prize[1].split("=")[1]) + 10000000000000  # Corrected Y value

            machines.append(
                {
                    "A": {"x": a_x, "y": a_y},
                    "B": {"x": b_x, "y": b_y},
                    "prize": {"x": p_x, "y": p_y},
                }
            )
    return machines


def solve_machine(machine):
    a_x, a_y = machine["A"]["x"], machine["A"]["y"]
    b_x, b_y = machine["B"]["x"], machine["B"]["y"]
    p_x, p_y = machine["prize"]["x"], machine["prize"]["y"]

    # Solve as linear equations
    # ax1 + bx2 = px
    # ay1 + by2 = py

    det = a_x * b_y - a_y * b_x
    if det == 0:
        return None  # No unique solution, lines are parallel

    det_a = p_x * b_y - p_y * b_x
    det_b = a_x * p_y - a_y * p_x

    # Solve for presses of A and B
    presses_a = det_a / det
    presses_b = det_b / det

    # Check if solutions are integers
    if presses_a.is_integer() and presses_b.is_integer():
        presses_a = int(presses_a)
        presses_b = int(presses_b)

        if presses_a >= 0 and presses_b >= 0:
            cost = presses_a * 3 + presses_b
            return cost

    return None


def main():
    machines = parse_input("input.txt")
    total_cost = 0
    prizes_won = 0

    for machine in machines:
        result = solve_machine(machine)
        if result is not None:
            total_cost += result
            prizes_won += 1

    print(f"Prizes won: {prizes_won}")
    print(f"Total cost: {total_cost}")


if __name__ == "__main__":
    main()
