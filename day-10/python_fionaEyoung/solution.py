import numpy as np

STEPDIRS = np.array([[1, 0], [-1, 0], [0, 1], [0, -1]])

def walk_trail(map, start):

  peaks = []
  el = map[tuple(start)]

  steps = start + STEPDIRS

  steps = steps[~np.logical_or(
    (steps<0).any(axis=1),
    (steps>=map.shape).any(axis=1))] # dont go off the map

  next = map[tuple(steps.T)]

  for elevation, pos in zip(next, steps):
    if elevation == el+1:
      if elevation == 9:
        peaks.append(pos)
      else:
        peaks.extend(walk_trail(map, pos))

  return peaks

fname = 'input.txt'

with open(fname, 'r') as f:
  lines = f.readlines()

map = np.array([[100 if c=='.' else int(c) for c in line.strip()] for line in lines])

trailheads = np.argwhere(map==0)

scores, ratings = 0, 0


for head in trailheads:
  trails = walk_trail(map, head)
  scores += len(np.unique(np.array(trails), axis=0))
  ratings += len(trails)

print("Part 1: ", scores )
print("Part 2: ", ratings)
