def read_input(file_path):
    """Reads and parses the input file with error handling for blank lines."""
    with open(file_path, "r") as file:
        lines = [line.strip() for line in file if line.strip()]  # Remove empty lines

    if len(lines) < 4:
        raise ValueError(
            "Input file is missing required lines. Ensure it contains four lines."
        )

    try:
        # Parse initial register values
        register_a = int(lines[0].split(":")[1].strip())
        register_b = int(lines[1].split(":")[1].strip())
        register_c = int(lines[2].split(":")[1].strip())
    except (IndexError, ValueError):
        raise ValueError("Error parsing register values. Ensure the format is correct.")

    try:
        # Parse program instructions
        program = list(map(int, lines[3].split(":")[1].strip().split(",")))
    except (IndexError, ValueError):
        raise ValueError(
            "Error parsing program instructions. Ensure the program line is formatted correctly."
        )

    return register_a, register_b, register_c, program


def get_combo_value(operand, registers):
    """Calculates the value of a combo operand."""
    if operand <= 3:
        return operand
    elif operand == 4:
        return registers["A"]
    elif operand == 5:
        return registers["B"]
    elif operand == 6:
        return registers["C"]
    else:
        raise ValueError("Invalid combo operand.")


def execute_program(register_a, register_b, register_c, program):
    """Executes the program and returns the output."""
    registers = {"A": register_a, "B": register_b, "C": register_c}
    output = []
    pointer = 0

    while pointer < len(program):
        opcode = program[pointer]
        operand = program[pointer + 1] if pointer + 1 < len(program) else 0

        if opcode == 0:  # adv
            denominator = 2 ** get_combo_value(operand, registers)
            registers["A"] //= denominator

        elif opcode == 1:  # bxl
            registers["B"] ^= operand

        elif opcode == 2:  # bst
            registers["B"] = get_combo_value(operand, registers) % 8

        elif opcode == 3:  # jnz
            if registers["A"] != 0:
                pointer = operand
                continue

        elif opcode == 4:  # bxc
            registers["B"] ^= registers["C"]

        elif opcode == 5:  # out
            output.append(get_combo_value(operand, registers) % 8)

        elif opcode == 6:  # bdv
            denominator = 2 ** get_combo_value(operand, registers)
            registers["B"] = registers["A"] // denominator

        elif opcode == 7:  # cdv
            denominator = 2 ** get_combo_value(operand, registers)
            registers["C"] = registers["A"] // denominator

        else:
            raise ValueError("Invalid opcode.")

        pointer += 2

    return output


def find_a_by_digit_matching(initial_b, initial_c, program):
    """Finds the lowest positive value for register A by matching output digits progressively."""
    target_output = program  # The program is the target output
    num_digits = len(target_output)
    candidate_a = 8**15  # Start with a large base value
    step = 8**15  # Start with a large step size

    for digit_index in range(num_digits - 1, -1, -1):  # Start from the last digit
        print(f"Matching last {num_digits - digit_index} digits...")
        found = False

        while not found:
            output = execute_program(candidate_a, initial_b, initial_c, program)
            if (
                output[-(num_digits - digit_index) :]
                == target_output[-(num_digits - digit_index) :]
            ):
                # Match found for current digit(s)
                found = True
            else:
                candidate_a += step  # Increment to search for the next value

        # Refine step to match earlier digit(s) in subsequent iterations
        step //= 8

    return candidate_a


if __name__ == "__main__":
    # Read input
    input_file = "input.txt"
    register_a, register_b, register_c, program = read_input(input_file)

    # Part 1: Execute program and get output
    part1_output = execute_program(register_a, register_b, register_c, program)
    print("Part 1 Output:", ",".join(map(str, part1_output)))

    # Part 2: Search for lowest A using digit matching
    try:
        lowest_a = find_a_by_digit_matching(register_b, register_c, program)
        print("Part 2 Lowest A:", lowest_a)
    except ValueError as e:
        print(e)
