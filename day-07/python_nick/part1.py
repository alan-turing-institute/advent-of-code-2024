

testinput = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""

def get_input(test=False):
    answers = []
    operands = []
    if test:
        inputlines = testinput.split("\n")
    else:
        inputlines = open("input.txt", "r").readlines()
    for line in inputlines:
        answers.append(int(line.split(":")[0]))
        operands.append([int(x.strip()) for x in line.split(":")[1].split(" ")[1:]])
    return answers, operands


def is_correct(answer, eqn):
    return eval(eqn) == answer


def add_next(eqn_so_far, next_number):
    return f"{eval(eqn_so_far)} + {next_number}"

def multiply_next(eqn_so_far, next_number):
    return f"{eval(eqn_so_far)} * {next_number}"


def equation_builder(answer, operands):
    possible_eqns = {0: [f"{operands[0]}"]}
    for i in range(1, len(operands)):
        possible_eqns[i] = []
        for eqn in possible_eqns[i-1]:
            next_add = add_next(eqn, operands[i])
            possible_eqns[i].append(next_add)
            next_multiply = multiply_next(eqn, operands[i])
#            print(f"next add {next_add} next multiply {next_multiply}")
            possible_eqns[i].append(next_multiply)
    return possible_eqns[len(operands)-1]

total = 0
answers, operands = get_input(False)
for i in range(len(answers)):
    eqs = equation_builder(answers[i], operands[i])
    for eq in eqs:
        if is_correct(answers[i], eq):
            print(f"{eq} = {answers[i]} - add to total")
            total += answers[i]
            break


print(f"part 1: {total}")
