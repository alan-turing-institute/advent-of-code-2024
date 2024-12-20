from itertools import combinations

import numpy as np

with open("input.txt") as f:
    lines = f.read().splitlines()

grid = np.array([list(l) for l in lines])

directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]

# ===============================================
# it's a track --> there is only one way through it
# reconstruct track path in the right order
# ===============================================
spaces = tuple(np.argwhere(grid == "."))
curr_pos = tuple(np.argwhere(grid == "S")[0])
track = [curr_pos]
for _ in range(len(spaces) + 1):
    for direction in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
        new_pos = (curr_pos[0] + direction[0], curr_pos[1] + direction[1])
        if grid[new_pos[0]][new_pos[1]] == "." and new_pos not in track:
            curr_pos = new_pos
            track.append(curr_pos)
end_pos = tuple(np.argwhere(grid == "E")[0])
track.append(end_pos)

# ===============================================
# PART 1
# - check one wall at a time
# - if there are 2 track positions adjacent to the wall,
#   compute their distance on track --> this is the time
#   this cheat could save
# - remember that the cheat takes 2 picoseconds !
# ===============================================
count = 0
walls = tuple(np.argwhere(grid == "#"))
for wall in walls:
    # find positions on the track adjacent to the wall (if there are any)
    # their index tells us when they are visited and so the
    # distance/time between them
    adjacent_positions = []
    for direction in directions:
        new_pos = (wall[0] + direction[0], wall[1] + direction[1])
        if new_pos in track:
            adjacent_positions.append(track.index(new_pos))
    # ignore cases where:
    # - wall is not track adjacent
    # - only one part of track is wall adjacent
    # - wall is adjacent to 3 track positions (it's a corner)
    # does this cheat save at least 100 picoseconds of time?
    if len(adjacent_positions) == 2:
        if abs(adjacent_positions[0] - adjacent_positions[1]) - 2 >= 100:
            count += 1

print(count)


# ===============================================
# PART 2
# - same as before but now can cheat for 20 picoseconds
# - rather than removing walls, compare pairs of track positions
# - can we get them closer by cheating?
# ===============================================

# avoid having to recalculate track index for positions at each step to speed up
travel_time = {pos: i for i, pos in enumerate(track)}

count = 0
for i, pos1 in enumerate(track):
    for j, pos2 in enumerate(track[i:]):
        # distance on grid between positions has to fit within the cheat
        dist = abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
        if dist <= 20:
            # is the time travelled sufficiently reduced with this cheat
            # (taking into account the cheat penalty)
            if abs(travel_time[pos1] - travel_time[pos2]) - dist >= 100:
                count += 1
print(count)
