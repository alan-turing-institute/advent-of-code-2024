def parse_disk_map(disk_map):
    files = []
    free_spaces = []

    for i in range(0, len(disk_map) - 1, 2):  # Ensure we don't go out of range
        file_length = int(disk_map[i])
        free_space_length = int(disk_map[i + 1])
        files.append(file_length)
        free_spaces.append(free_space_length)

    # Handle case where the last digit is a file length without a corresponding free space length
    if len(disk_map) % 2 == 1:
        files.append(int(disk_map[-1]))
        free_spaces.append(0)  # No free space after the last file

    return files, free_spaces


def calculate_checksum(files):
    position = 0
    checksum = 0

    for file_id, file_length in enumerate(files):
        for _ in range(file_length):
            checksum += position * file_id
            position += 1

    return checksum


def main():
    # Read input from file
    with open("input.txt", "r") as f:
        disk_map = f.read().strip()

    files, free_spaces = parse_disk_map(disk_map)

    # Compact disk directly and calculate checksum
    checksum = calculate_checksum(files)

    print("Filesystem checksum:", checksum)


if __name__ == "__main__":
    main()
