def can_evaluate_to_target(target, numbers, current_value=0, index=0):
    """
    Determines if the numbers can be combined with +, *, or || to produce the target value.
    Uses recursive backtracking for efficiency.
    """
    if index == len(numbers):  # Base case: no more numbers to process
        return current_value == target

    # Take the next number
    num = numbers[index]

    # Try addition
    if can_evaluate_to_target(target, numbers, current_value + num, index + 1):
        return True

    # Try multiplication
    if can_evaluate_to_target(
        target, numbers, current_value * num if index > 0 else num, index + 1
    ):
        return True

    # Try concatenation
    if index > 0:  # Concatenation only makes sense if there's a prior value
        concatenated = int(str(current_value) + str(num))
        if can_evaluate_to_target(target, numbers, concatenated, index + 1):
            return True

    return False


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
            if can_evaluate_to_target(target, numbers):
                total += target
    return total


# Main execution
if __name__ == "__main__":
    input_file = "input.txt"
    total_calibration_result = calculate_total_calibration(input_file)
    print(f"Total Calibration Result: {total_calibration_result}")
