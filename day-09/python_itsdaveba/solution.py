import numpy as np

with open("input.txt") as file:
    input = file.read()

disk_map = list(map(int, input))
FREE_SPACE = -1

# PART ONE

layout = []
for i, digit in enumerate(disk_map):
    if i % 2 == 0:
        id_number = i // 2
        layout.extend([id_number] * digit)
    else:
        layout.extend([FREE_SPACE] * digit)

new_layout = layout.copy()
left, right = 0, len(layout) - 1  # two pointers
while left < right:
    if new_layout[left] == FREE_SPACE:
        new_layout[left] = new_layout[right]  # assume the disk_map ends with a file
        right -= 1
        while new_layout[right] == FREE_SPACE:
            right -= 1
    left += 1

checksum = 0
for i, id_number in enumerate(new_layout[: right + 1]):
    checksum += i * id_number

print("Part One:", checksum)


# PART TWO

# now we need to check `disk_map` because we are moving complete files
new_layout = np.array(layout)
starting_block = np.cumsum(disk_map)
file_blocks = [(int(index), num_blocks) for index, num_blocks in zip(starting_block[1::2], disk_map[2::2])]  # index, num_blocks
free_blocks = [(int(index), num_blocks) for index, num_blocks in zip(starting_block[0::2], disk_map[1::2])]  # index, num_blocks
while file_blocks:
    file_index, file_size = file_blocks.pop()
    for i, (free_index, free_size) in enumerate(free_blocks):
        if free_index >= file_index:
            break
        if free_size >= file_size:
            new_layout[free_index: free_index + file_size] = new_layout[file_index: file_index + file_size]
            new_layout[file_index: file_index + file_size] = FREE_SPACE
            free_blocks[i] = (free_index + file_size, free_size - file_size)
            break

checksum = 0
for i, id_number in enumerate(new_layout):
    if id_number != FREE_SPACE:
        checksum += i * id_number

print("Part Two:", checksum)
