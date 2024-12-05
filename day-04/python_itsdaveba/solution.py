import numpy as np

with open("input.txt") as file:
    input = np.array([list(line) for line in file.read().splitlines()])


# Part One

n_rows, n_cols = input.shape

target = "XMAS"
total = 0

for row in input:
    total += "".join(row).count(target)
    total += "".join(np.flip(row)).count(target)

for col in input.T:
    total += "".join(col).count(target)
    total += "".join(np.flip(col)).count(target)

for offset in range(-n_rows + 1, n_cols):
    diag = input.diagonal(offset)
    total += "".join(diag).count(target)
    total += "".join(np.flip(diag)).count(target)

for offset in range(-n_cols + 1, n_rows):
    diag = np.rot90(input).diagonal(offset)
    total += "".join(diag).count(target)
    total += "".join(np.flip(diag)).count(target)

print(total)


# Part Two
total = 0
mask = np.eye(3, dtype=bool) ^ np.rot90(np.eye(3, dtype=bool))  # Mask the corners of the 3x3 grid
reorder = [[0, 3], [1, 2]]  # Reorder mask from cross to rows
for i in range(1, n_rows - 1):
    for j in range(1, n_cols - 1):
        if input[i, j] == "A":  # 3x3 grid with a centered `A`
            block = input[i-1:i+2, j-1:j+2]
            block[mask][reorder]
            # Check if any of the diagonals has `M` and `S`
            xmas = np.any(np.isin(block[mask][reorder], "M"), axis=1) & np.any(np.isin(block[mask][reorder], "S"), axis=1)
            total += np.all(xmas)

print(total)
