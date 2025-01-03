import math


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
            p_x = int(prize[0].split("=")[1])  # Extract X value after 'X='
            p_y = int(prize[1].split("=")[1])  # Extract Y value after 'Y='

            machines.append(
                {
                    "A": {"x": a_x, "y": a_y},
                    "B": {"x": b_x, "y": b_y},
                    "prize": {"x": p_x, "y": p_y},
                }
            )
    return machines


def solve_machine(machine, max_presses=100):
    a_x, a_y = machine["A"]["x"], machine["A"]["y"]
    b_x, b_y = machine["B"]["x"], machine["B"]["y"]
    p_x, p_y = machine["prize"]["x"], machine["prize"]["y"]

    min_cost = math.inf
    best_combination = None

    for a_presses in range(max_presses + 1):
        for b_presses in range(max_presses + 1):
            total_x = a_presses * a_x + b_presses * b_x
            total_y = a_presses * a_y + b_presses * b_y

            if total_x == p_x and total_y == p_y:
                cost = a_presses * 3 + b_presses
                if cost < min_cost:
                    min_cost = cost
                    best_combination = (a_presses, b_presses)

    return min_cost if best_combination else None


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
