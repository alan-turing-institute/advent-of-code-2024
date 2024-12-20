import numpy as np

with open("input.txt") as f:
    lines = f.read().splitlines()

grid = np.array([list(l) for l in lines])

# ===============================================
# it's a track --> each space gets visited once
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
#   compute their distance on track
# - remember there is a 2 point penalty for cheating !
# ===============================================
count = 0
walls = tuple(np.argwhere(grid == "#"))
for wall in walls:
    # find the parts of track next to the wall (if there are any)
    # and store the index of those locations on the track
    adjacent_positions = []
    for direction in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
        new_pos = (wall[0] + direction[0], wall[1] + direction[1])
        if new_pos in track:
            adjacent_positions.append(track.index(new_pos))
    # ignore cases where:
    # - wall is not track adjacent
    # - only one part of track is wall adjacent
    # - wall is adjacent to 3 track positions (it's a corner)
    if len(adjacent_positions) == 2:
        if abs(adjacent_positions[0] - adjacent_positions[1]) - 2 >= 100:
            count += 1

print(count)
