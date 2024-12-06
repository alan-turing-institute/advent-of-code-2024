from collections import Counter


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


def calculate_similarity_score(left_list, right_list):
    """
    Calculate the similarity score between two lists.
    The similarity score is the sum of each number in the left list multiplied
    by the number of times it appears in the right list.

    Args:
    left_list (list): First list of numbers.
    right_list (list): Second list of numbers.

    Returns:
    int: Total similarity score.
    """
    # Count occurrences of each number in the right list
    right_counts = Counter(right_list)

    # Calculate the similarity score
    similarity_score = sum(num * right_counts[num] for num in left_list)

    return similarity_score


# Example usage
if __name__ == "__main__":
    # Path to the input file
    file_path = "input.txt"  # Replace with your actual file path

    # Read the lists from the file
    left_list, right_list = read_lists_from_file(file_path)

    # Calculate the similarity score
    similarity_score = calculate_similarity_score(left_list, right_list)

    print(f"Similarity score: {similarity_score}")
