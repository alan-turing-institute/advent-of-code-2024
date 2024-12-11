from itertools import product


def evaluate_equation(target, numbers):
    """
    Determines if the numbers can be combined with + and * to produce the target value.
    """
    n = len(numbers)
    # Generate all combinations of operators (+ and *)
    for operators in product("+-*", repeat=n - 1):
        expression = str(numbers[0])
        for i in range(n - 1):
            expression += f" {operators[i]} {numbers[i + 1]}"
        # Evaluate the expression left to right
        if evaluate_left_to_right(expression) == target:
            return True
    return False


def evaluate_left_to_right(expression):
    """
    Evaluates an expression from left to right, ignoring normal operator precedence.
    """
    tokens = expression.split()
    result = int(tokens[0])
    index = 1
    while index < len(tokens):
        operator = tokens[index]
        operand = int(tokens[index + 1])
        if operator == "+":
            result += operand
        elif operator == "*":
            result *= operand
        index += 2
    return result


def calculate_total_calibration(file_path):
    """
    Reads input, processes the equations, and calculates the total calibration result.
    """
    total = 0
    with open(file_path, "r") as file:
        for line in file:
            if ":" not in line:
                continue
            target, numbers = line.strip().split(":")
            target = int(target)
            numbers = list(map(int, numbers.split()))
            if evaluate_equation(target, numbers):
                total += target
    return total


# Main execution
if __name__ == "__main__":
    input_file = "input.txt"
    total_calibration_result = calculate_total_calibration(input_file)
    print(f"Total Calibration Result: {total_calibration_result}")
