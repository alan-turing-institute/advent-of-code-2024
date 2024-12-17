import numpy
import os
import math


def parse_file(file_path):
    with open(os.path.join(file_path)) as f:
        lines = f.read().splitlines()

    register = {}
    for a in lines:
        if a == "":
            continue
        if a.split(": ")[0] != "Program":
            register[a.split(": ")[0]] = int(a.split(": ")[1])
        else:
            register[a.split(": ")[0]] = a.split(": ")[1].split(", ")

    return register


def get_combo(input, register):
    """Get the combo value based on the input."""
    if input >= 0 and input <= 3:
        return input
    elif input == 4:
        return register['Register A']
    elif input == 5:
        return register['Register B']
    elif input == 6:
        return register['Register C']
    else:
        return None


def adv(register, combo):
    register['Register A'] = int(register['Register A'] / (2 ** combo))
    return register


def bxl(register, input):
    register['Register B'] = register['Register B'] ^ input
    return register


# The bst instruction (opcode 2) calculates the value of its combo operand modulo 8
def bst(register, combo):
    register['Register B'] = combo % 8
    return register


def jzn(register, input):
    if register['Register A'] == 0:
        return register
    else:
        return input


def bxc(register, input):
    register['Register B'] = register['Register B'] ^ register['Register C']
    return register


def out(combo):
    return combo % 8


def bdv(register, combo):
    register['Register B'] = int(register['Register A'] / (2 ** combo))
    return register


def cdv(register, combo):
    register['Register C'] = int(register['Register A'] / (2 ** combo))
    return register


def program_logic(opcode, operand, register):
    """Run the program logic based on the opcode."""
    combo = get_combo(operand, register)
    if opcode == 0:
        return adv(register, combo)
    elif opcode == 1:
        return bxl(register, operand)
    elif opcode == 2:
        return bst(register, combo)
    elif opcode == 3:
        return jzn(register, operand)
    elif opcode == 4:
        return bxc(register, operand)
    elif opcode == 5:
        return out(combo)
    elif opcode == 6:
        return bdv(register, combo)
    elif opcode == 7:
        return cdv(register, combo)


def run_program(program, register, start_index=0, output=None):
    """Run the program and return the output."""
    if output is None:
        output = []
    again = False
    for index in range(start_index, len(program), 2):

        opcode = int(program[index])
        operand = int(program[index + 1])

        result = program_logic(opcode, operand, register)

        if isinstance(result, dict):
            register = result
        elif opcode != 3:
            output.append(result)
        else:
            start_index = operand
            again = True
            break

    if again:
        return run_program(program, register, start_index, output)
    else:
        return output


def get_match_program(register, match_indexes=24, initial_range=8 ** 15):
    """Find the minimum Register A value matching the program output."""
    program = register['Program'][0].split(',')
    target_output = ",".join(program)

    step = 8 ** (match_indexes // 2)
    for value in range(initial_range, 8 ** len(program), step):
        register['Register A'] = value
        output = run_program(program, register.copy())
        output_str = ",".join(map(str, output))

        if output_str[match_indexes:] == target_output[match_indexes:]:
            if match_indexes == 0:
                return value
            return get_match_program(register, match_indexes - 2, value)


if __name__ == "__main__":
    file_name = "input.txt"
    # file_name = "test2.txt"

    data = parse_file(file_name)
    program = data['Program'][0].split(',')

    output = run_program(program, data.copy())
    output = ",".join([str(x) for x in output])

    print("Part 1:", output)

    # start matching the last item in the program, multiply by 2 because i'm matching strings that include commas as above
    match = (len(program) -1)*2

    # start with range 8**15 and 8**16
    min_A = get_match_program(data, match_indexes=match, initial_range=8 ** 15)

    print("Part 2:", min_A)
