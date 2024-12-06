def is_safe_report(report):
    """
    Determines if a report is safe.
    A report is safe if:
    1. Levels are either all increasing or all decreasing.
    2. Any two adjacent levels differ by at least 1 and at most 3.
    """
    # Calculate differences between consecutive levels
    differences = [report[i + 1] - report[i] for i in range(len(report) - 1)]

    # Check if all differences are either positive or negative
    increasing = all(1 <= diff <= 3 for diff in differences)
    decreasing = all(-3 <= diff <= -1 for diff in differences)

    # Report is safe if it's either all increasing or all decreasing
    return increasing or decreasing


def is_safe_with_dampener(report):
    """
    Determines if a report is safe with the Problem Dampener.
    The Problem Dampener allows removing one level to make an unsafe report safe.
    """
    if is_safe_report(report):
        return True  # Already safe without any removal

    # Try removing each level one at a time and check if the remaining report is safe
    for i in range(len(report)):
        modified_report = report[:i] + report[i + 1 :]  # Remove the i-th level
        if is_safe_report(modified_report):
            return True

    return False  # Not safe even with the Problem Dampener


def count_safe_reports_with_dampener(file_path):
    """
    Reads data from a file and counts the number of safe reports with the Problem Dampener.
    Each line in the file is a space-separated list of integers.
    """
    safe_count = 0
    with open(file_path, "r") as file:
        for line in file:
            report = list(map(int, line.strip().split()))
            if is_safe_with_dampener(report):
                safe_count += 1
    return safe_count


# File path to the input data
file_path = "input.txt"

# Count and print the number of safe reports with the Problem Dampener
safe_reports = count_safe_reports_with_dampener(file_path)
print(f"Number of safe reports with the Problem Dampener: {safe_reports}")
