"""
Advent of Code 2024
Day 09
tomogwen
"""
from pathlib import Path


def parse_file(file_path):
    file_bool, file_idx = True, 0
    disk = []
    with open(file_path, 'r') as file:
         while True:
            # read and process character
            char = file.read(1)
            if not char or char == "\n":
                break
            else:
                char = int(char)

            # add to disk
            if file_bool:
                for _ in range(char):
                    disk.append(file_idx)
                file_idx += 1
                file_bool = False
            else:
                for _ in range(char):
                    disk.append(-1)
                file_bool = True
    return disk


def part_one(disk):
    free_space = disk.count(-1)
    for idx in range(len(disk)-1, -1, -1):
        first_free_space = disk.index(-1)
        if first_free_space == len(disk) - free_space:
            break
        if disk[idx] != -1:            
            disk[first_free_space] = disk[idx]
            disk[idx] = -1
    return disk


def checksum(disk):
    sum = 0
    for idx, element in enumerate(disk):
        if element != -1:
            sum += element * idx
    return sum


def find_free_space(disk):
    """Return list of pairs of numbers representing start and length of free sections."""
    free_space = []
    in_free = False
    for idx, value in enumerate(disk):
        if not in_free and value == -1:
            in_free = True
            free_space.append([idx, -1])
        if in_free and value != -1:
            in_free = False
            free_space[-1][1] = idx - free_space[-1][0]
    return free_space


def find_file_block(id, disk):
    """Returns left-most index and length of file by ID."""
    start = disk.index(id)
    for idx in range(start+1, len(disk)+1):
        # handle final block on disk
        if idx == len(disk):
            return start, len(disk)-start
        # handle other blocks
        elif disk[idx] != id:
            return start, idx-start
        

def part_two(disk):
    for file_id in range(max(disk), 1, -1):
        file_idx, file_len = find_file_block(file_id, disk)
        for left_idx, space_len in find_free_space(disk):
            if file_len <= space_len and left_idx < file_idx:
                # move file
                for i in range(file_len):
                    disk[left_idx+i] = disk[file_idx+i]
                    disk[file_idx+i] = -1
                break
    return disk


if __name__ == "__main__":
    file_path = Path("input.txt")
    disk = parse_file(file_path)    

    disk_one = part_one(disk.copy())
    part_one_answer = checksum(disk_one)
    
    disk_two = part_two(disk)
    part_two_answer = checksum(disk_two)
    
    print("Part 1 solution:", part_one_answer)
    print("Part 2 solution:", part_two_answer)
