import numpy
import os
import math
import numpy as np

def parse_file(file_path):
    with open(os.path.join(file_path)) as f:
        lines = f.read().splitlines()
    return lines

def read_robots(data):
    robots = []
    for index, line in enumerate(data):
        if "p" in line:
            l = line.split(",")
            p0x = int(l[0][2:])
            p0y = int(l[1].split(" ")[0])
            vx = int(l[1].split(" ")[1][2:])
            vy = int(l[2])

            robots_i = {}
            robots_i[str(index)] = {
                "p": [[p0x, p0y]],
                "v": [vx, vy]
            }
            robots.append(robots_i)
    return robots

def move_robots(robots, x, y):

    for robot in robots:
        for key, value in robot.items():
            p = value["p"][-1]
            v = value["v"]

            new_p = [p[0] + v[0], p[1]+ v[1]]
            new_p = check_borders(new_p, x, y)
            robot[key]["p"].append(new_p)

    return robots

def check_borders(pos, x,y):
    if pos[0] >= x or pos[0] < 0:
        pos[0] = pos[0] % x
    if pos[1] >= y or pos[1] < 0:
        pos[1] = pos[1] % y

    return pos

def plot_robots(robots, x, y):
    plot = numpy.zeros((y,x))
    for robot in robots:
        for key, value in robot.items():
            p = value["p"][-1]
            plot[p[1], p[0]] = plot[p[1], p[0]] +1
    return plot


if __name__ == "__main__":

    file_name = "input.txt"
    #file_name = "test.txt"

    data = parse_file(file_name)

    robots = read_robots(data)

    x = 101
    y = 103
    seconds = 100000
    for i in range(0, seconds):
        robots = move_robots(robots,x,y)
        plot = plot_robots(robots, x, y)

        if np.max(plot)==1:
            print("Part 2: Chritsmas tree found at second ", i+1)
            break
        if i == 99:
            plot_part1 = plot



    mid_x = x // 2
    mid_y = y // 2

    top_left = plot_part1[:mid_y, :mid_x]
    top_right = plot_part1[mid_y + 1:, :mid_x]
    bottom_left = plot_part1[:mid_y, mid_x + 1:]
    bottom_right = plot_part1[mid_y + 1:, mid_x + 1:]


    total = numpy.sum(top_left)* numpy.sum(top_right)* numpy.sum(bottom_left)* numpy.sum(bottom_right)

    print("Part 1: ", total)
