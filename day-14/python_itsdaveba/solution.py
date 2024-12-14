import re
import numpy as np

with open("input.txt") as file:
    input = file.read()

TIME = 100
SPACE = np.array((101, 103))

# get to the bathroom
# swarmed with robots
# robots move in straight lines
# position and velocities
# 101 tiles wide and 103 tiles tall
# test 11 tiles wide and 7 tiles tall
# they can teleport
# position after 100 seconds
# count the number of robots in each quadrant after 100 seconds
# Multiplying these together gives a total safety factor

pattern = r"-?\d+,-?\d+"
p = re.compile(pattern)

positions, velocities = [], []
for line in input.splitlines():
    pos, vel = [list(map(int, pair.split(","))) for pair in p.findall(line)]
    positions.append(pos)
    velocities.append(vel)

positions = np.array(positions)
velocities = np.array(velocities)

# Part Two
# with open("output.txt", "w") as file:
#     for t in range(7503):
#         space_map = np.zeros(SPACE, dtype=bool)
#         space_map[positions[:, 0], positions[:, 1]] = True
#         file.write(str(t) + "\n")
#         for row in space_map.T:
#             for col in row:
#                 file.write("#" if col else ".")
#             file.write("\n")
#         positions += velocities
#         positions %= SPACE

positions += velocities * TIME
positions %= SPACE

safety_factor = np.zeros((2, 2), dtype=int)
middle = SPACE // 2
for pos in positions:
    if np.all(pos != middle):
        quadrant = np.where(pos < middle, 1, 0)
        safety_factor[tuple(quadrant)] += 1

print("Part One:", safety_factor.prod())
