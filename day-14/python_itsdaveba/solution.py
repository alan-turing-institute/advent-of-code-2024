import re
import numpy as np

with open("input.txt") as file:
    input = file.read()

TIME = 100
SPACE = np.array((101, 103))

pattern = r"-?\d+,-?\d+"
p = re.compile(pattern)

positions, velocities = [], []
for line in input.splitlines():
    pos, vel = [list(map(int, pair.split(","))) for pair in p.findall(line)]
    positions.append(pos)
    velocities.append(vel)

positions = np.array(positions)
velocities = np.array(velocities)

positions += velocities * TIME
positions %= SPACE

safety_factor = np.zeros((2, 2), dtype=int)
middle = SPACE // 2
for pos in positions:
    if np.all(pos != middle):
        quadrant = np.where(pos < middle, 1, 0)
        safety_factor[tuple(quadrant)] += 1

print("Part One:", safety_factor.prod())
