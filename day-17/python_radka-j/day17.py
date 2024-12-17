def get_combo(operand, registers):
    if operand >= 0 and operand <= 3:
        return operand
    elif operand == 4:
        return registers["A"]
    elif operand == 5:
        return registers["B"]
    elif operand == 6:
        return registers["C"]
    else:
        return None


def execute_instruction(opcode, operand, registers):
    combo = get_combo(operand, registers)
    if opcode == 0:
        registers["A"] = int(registers["A"] / (2**combo))
    elif opcode == 1:
        registers["B"] = registers["B"] ^ operand
    elif opcode == 2:
        registers["B"] = combo % 8
    # do not increase instruction pointer if A is 0
    elif opcode == 3:
        if registers["A"] != 0:
            return "jump"
    elif opcode == 4:
        registers["B"] = registers["B"] ^ registers["C"]
    # the out operator is opcode 5
    elif opcode == 5:
        return combo % 8
    elif opcode == 5:
        registers["B"] = int(registers["A"] / (2**combo))
    elif opcode == 7:
        registers["C"] = int(registers["A"] / (2**combo))
    return registers


def run_program(registers):
    # excecute each instruction and save output values
    instruction_pointer = 0
    outputs = []

    while instruction_pointer < len(program):
        opcode = int(program[instruction_pointer])
        operand = int(program[instruction_pointer + 1])
        output = execute_instruction(opcode, operand, registers)

        # got an out instruction
        if opcode == 5:
            outputs.append(output)

        # increment pointer
        if output == "jump":
            instruction_pointer = operand
        else:
            instruction_pointer += 2
    return outputs


# PART 1
# opcode, operand, opcode, operand...
program = [2, 4, 1, 5, 7, 5, 1, 6, 4, 3, 5, 5, 0, 3, 3, 0]
outputs = run_program({"A": 47792830, "B": 0, "C": 0})
print("PART 1: ", ",".join([str(val) for val in outputs]))

# PART 2

# in each column of the output the numbers change at a different rate:
# - zero col -> change every 1 step --> 8**0
# - first col -> change every 8 steps --> 8**1
# - second col -> change every 64 steps --> 8**2
# - third col -> change every 512 steps --> 8**3
# - ...
# - 15th col -> 8 ** 15

# start with the first number that returns a 16 length output
stack = [(8**15, 15)]

while stack:
    # sort to get the lowest A value available
    stack = sorted(stack, key=lambda x: x[0], reverse=True)
    curr_A, index = stack.pop()
    step_size = 8**index
    # with curr_A we've matched [index+1:] values of the program
    # we've now moved down an index and step through from curr_A up to a value at which
    # the last n program values remain matched -  check for a match at current index
    for value in range(curr_A, curr_A + 8 ** (index + 1) + step_size + 1, step_size):
        output = run_program({"A": value, "B": 0, "C": 0})
        if output[index:] == program[index:]:
            if index == 0:
                print("PART 2: ", value)
                # no need to look for additional A values that also return program
                stack = []
                break
            else:
                stack.append((value, index - 1))
