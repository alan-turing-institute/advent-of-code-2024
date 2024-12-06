import numpy as np

def find_next_event(map, position, direction):
  x, y = position

  if direction == 'up':
    path = map[:x, y]
    inds = np.nonzero(path)[0]
    if inds.size > 0:
      obstacle = inds[-1]
      new_pos = (obstacle+1, y)
      new_direction = 'right'
      visited = (slice(obstacle, x), y)
    else:
      new_pos = (0, y)
      new_direction = 'up'
      visited = (slice(0, x), y)

  elif direction == 'down':
    path = map[x:, y]
    inds = np.nonzero(path)[0]
    if inds.size > 0:
      obstacle = x+inds[0]
      new_pos = (obstacle-1, y)
      new_direction = 'left'
      visited = (slice(x, obstacle), y)
    else:
      new_pos = (-1, y)
      new_direction = 'down'
      visited = (slice(x, -1), y)

  if direction == 'right':
    path = map[x, y:]
    inds = np.nonzero(path)[0]
    if inds.size > 0:
      obstacle = y+inds[0]
      new_pos = (x, obstacle-1)
      new_direction = 'down'
      visited = (x, slice(y, obstacle))
    else:
      new_pos = (0, y)
      new_direction = 'up'
      visited = (x, slice(y, -1))

  if direction == 'left':
    path = map[x, :y]
    inds = np.nonzero(path)[0]
    if inds.size > 0:
      obstacle = inds[-1]
      new_pos = (x, obstacle+1)
      new_direction = 'up'
      visited = (x, slice(obstacle, y))
    else:
      new_pos = (x, 0)
      new_direction = 'left'
      visited = (x, slice(0, y))

  return new_pos, new_direction, visited

def main():

  fname = 'input.txt'

  with open(fname, 'r') as f:
    lines = f.readlines()

  char_map = np.array([[char for char in line.strip()] for line in lines])

  # guard = '^'

  guard = np.nonzero(np.logical_and(char_map!='#', char_map!='.'))
  guard = guard[0][0], guard[1][0]

  map = char_map=='#'
  direction = 'up'
  exit_flag = False

  visited_map = np.zeros(map.shape, dtype=bool)

  while not exit_flag:
    guard, new_direction, visited = find_next_event(map, guard, direction)
    visited_map[visited] = True
    exit_flag = new_direction == direction
    direction = new_direction

  visited_map[guard] = True
  # print(np.logical_and(visited_map, np.logical_not(map)))
  print("Part 1: ", np.logical_and(visited_map, np.logical_not(map)).sum())

if __name__ == '__main__':
  main()
