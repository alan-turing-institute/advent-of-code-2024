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

    return ",".join(map(str, output))


if __name__ == "__main__":
    # Read input
    input_file = "input.txt"
    register_a, register_b, register_c, program = read_input(input_file)

    # Execute program and get output
    result = execute_program(register_a, register_b, register_c, program)

    # Print the output
    print(result)
