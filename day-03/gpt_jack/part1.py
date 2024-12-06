import re


def extract_and_sum_mul(file_path):
    """
    Reads a file, extracts valid `mul(X,Y)` instructions, computes the results, and returns their sum.
    """
    total = 0
    pattern = (
        r"mul\(\s*(\d+)\s*,\s*(\d+)\s*\)"  # Regex to match valid mul(X,Y) instructions
    )

    with open(file_path, "r") as file:
        for line in file:
            matches = re.findall(pattern, line)
            for match in matches:
                x, y = map(int, match)  # Convert captured numbers to integers
                total += x * y

    return total


# Example usage:
if __name__ == "__main__":
    input_file = "input.txt"  # Replace with the path to your input file
    result = extract_and_sum_mul(input_file)
    print(f"Sum of all valid mul instructions: {result}")
