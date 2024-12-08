with open("input.txt") as file:
    input = file.read()

equations = input.splitlines()
operators = [lambda x, y: x + y, lambda x, y: x * y]  # add and multiply


# Part One

def dfs(value, index):
    if index >= length:
        if value == test_value:
            answer.append(test_value)
            return True
        return False
    for operator in operators:
        new_value = operator(value, numbers[index])
        if dfs(new_value, index + 1):
            return True
    return False

answer = []
for equation in equations:
    test_value, numbers = equation.split(":")
    test_value = int(test_value)
    numbers = [int(n) for n in numbers.split()]
    length = len(numbers)

    # DFS
    dfs(numbers[0], 1)

print("Part One:", sum(answer))


# Part Two

operators.append(lambda x, y: int(str(x) + str(y)))  # concatenate

answer = []
for equation in equations:
    test_value, numbers = equation.split(":")
    test_value = int(test_value)
    numbers = [int(n) for n in numbers.split()]
    length = len(numbers)

    # DFS
    dfs(numbers[0], 1)

print("Part Two:", sum(answer))
