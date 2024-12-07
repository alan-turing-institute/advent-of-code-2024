import re


def extract_and_sum_mul_with_conditions(file_path):
    """
    Reads a file, processes `mul(X,Y)` instructions with `do()` and `don't()` conditions,
    computes results for enabled multiplications, and returns their sum.
    """
    total = 0
    mul_enabled = True  # `mul` instructions are initially enabled
    # Regex patterns
    instruction_pattern = r"(do\(\)|don't\(\)|mul\(\s*\d+\s*,\s*\d+\s*\))"
    mul_pattern = r"mul\(\s*(\d+)\s*,\s*(\d+)\s*\)"
    do_pattern = r"do\(\)"
    dont_pattern = r"don't\(\)"

    with open(file_path, "r") as file:
        for line in file:
            # Extract instructions from the line
            instructions = re.findall(instruction_pattern, line)
            for instruction in instructions:
                # Handle state-changing instructions
                if re.match(do_pattern, instruction):
                    mul_enabled = True
                elif re.match(dont_pattern, instruction):
                    mul_enabled = False
                # Process `mul` instructions if enabled
                elif mul_enabled and re.match(mul_pattern, instruction):
                    match = re.match(mul_pattern, instruction)
                    x, y = map(int, match.groups())
                    total += x * y

    return total


# Example usage:
if __name__ == "__main__":
    input_file = "input.txt"  # Replace with the path to your input file
    result = extract_and_sum_mul_with_conditions(input_file)
    print(f"Sum of all enabled mul instructions: {result}")
