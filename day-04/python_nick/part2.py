import numpy as np

def is_x_mas(direction, puzzle, x, y, xsize, ysize):
    if x not in range(1,xsize-1) or y not in range(1,ysize-1):
        return False
    if puzzle[x-direction[0],y-direction[0]] == "M" and puzzle[x+direction[0],y+direction[0]] == "S" and \
       puzzle[x+direction[1],y-direction[1]] == "M" and puzzle[x-direction[1],y+direction[1]] == "S":
        return True


lines = []
for line in open("input.txt", "r").readlines():
    lines.append(list(line.strip()))

input_array = np.array(lines)
xsize = input_array.shape[0]
ysize = input_array.shape[1]

total = 0
for ix in range(xsize):
    for iy in range(ysize):
        if input_array[ix,iy] == "A":
            for direction in [(1,1),(1,-1),(-1,1),(-1,-1)]:
                if is_x_mas(direction, input_array, ix, iy, xsize, ysize):
                    total += 1

print(total)
