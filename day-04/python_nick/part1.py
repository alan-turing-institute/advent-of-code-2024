import numpy as np

def get_word(direction, puzzle, x, y, xsize, ysize):
    letters = [puzzle[x+i*direction[0],y+i*direction[1]] for i in range(4) \
               if (x+i*direction[0] in range(0,xsize) and y+i*direction[1] in range(0,ysize))]
    return "".join(letters)


def search_from_x(puzzle, x, y, xsize, ysize):
    directions = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
    num_xmas = 0
    for direction in directions:
        if get_word(direction, puzzle, x, y, xsize, ysize) == "XMAS":
            num_xmas += 1
    return num_xmas


lines = []
for line in open("input.txt", "r").readlines():
    lines.append(list(line.strip()))

input_array = np.array(lines)
xsize = input_array.shape[0]
ysize = input_array.shape[1]

total = 0
for ix in range(xsize):
    for iy in range(ysize):
        if input_array[ix,iy] == "X":
            total += search_from_x(input_array, ix, iy, xsize, ysize)

print(total)
