import re

with open("input.txt") as file:
    input = file.read()


register, program = input.split("\n\n")
register = {reg: int(val) for reg, val in [reg.split(": ") for reg in re.findall(r"[ABC]: \d+", register)]}  # {reg: value}
program = list(map(int, program.split(" ")[1].split(",")))  # list of opcodes and operands


def get_output(register, program):
    ip = 0  # instruction pointer
    output = []
    program_length = len(program)

    while ip < program_length:
        opcode, literal = program[ip: ip + 2]
        ip += 2

        # combo operand
        if 4 <= literal < 7:
            combo = register[chr(literal - 4 + ord("A"))]
        else:
            combo = literal

        # instructions
        match opcode:
            case 0:  # adv
                register["A"] >>= combo
            case 1:  # bxl
                register["B"] ^= literal
            case 2:  # bst
                register["B"] = combo % 8
            case 3:  # jnz
                if register["A"]:
                    ip = literal
            case 4:  # bxc
                register["B"] ^= register["C"]
            case 5:  # out
                output.append(combo % 8)
            case 6:  # bdv
                register["B"] = register["A"] >> combo
            case 7:  # cdv
                register["C"] = register["A"] >> combo

    return output


output = get_output(register, program)
output = map(str, output)

print("Part One:", ",".join(output))


value = 0
stack = [(value, len(program) - 1)]  # reg A value, target index
while stack:
    value, index = stack.pop()
    if index < 0:
        break
    target = program[index]
    for bits in range(7, -1, -1):
        next_value = value * 8 + bits
        register["A"] = next_value
        output = get_output(register, program)
        if output[0] == target:
            stack.append((next_value, index - 1))

print("Part Two:", value)
