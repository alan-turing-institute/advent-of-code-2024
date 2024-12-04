def read_lists_from_file(file_path):
    """
    Reads two lists of integers from a file with two columns.
    Each line contains a pair of integers: one for the left list and one for the right list.

    Args:
    file_path (str): Path to the input file.

    Returns:
    tuple: Two lists of integers (left_list, right_list).
    """
    left_list = []
    right_list = []

    with open(file_path, "r") as file:
        for line in file:
            left, right = map(int, line.strip().split())
            left_list.append(left)
            right_list.append(right)

    return left_list, right_list


def calculate_total_distance(left_list, right_list):
    """
    Calculate the total distance between two lists of numbers
    by pairing the smallest elements and summing their absolute differences.

    Args:
    left_list (list): First list of numbers.
    right_list (list): Second list of numbers.

    Returns:
    int: Total distance between the two lists.
    """
    # Sort both lists
    left_sorted = sorted(left_list)
    right_sorted = sorted(right_list)

    # Calculate the sum of absolute differences between paired elements
    total_distance = sum(abs(a - b) for a, b in zip(left_sorted, right_sorted))

    return total_distance


# Example usage
if __name__ == "__main__":
    # Path to the input file
    file_path = "input.txt"  # Replace with your actual file path

    # Read the lists from the file
    left_list, right_list = read_lists_from_file(file_path)

    # Calculate the total distance
    total_distance = calculate_total_distance(left_list, right_list)

    print(f"Total distance: {total_distance}")
