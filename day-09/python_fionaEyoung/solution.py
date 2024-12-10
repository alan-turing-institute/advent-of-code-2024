import numpy as np

BLANK = -1 # not np.nan, otherwise have to use floats everywhere

def explode_diskmap(files, spaces, result):

  idx = 0
  for i, (f, s) in enumerate(zip(files, spaces)):
    result[idx:idx+f] = i
    idx += f+s
  # end
  result[idx:idx+files[-1]] = len(files)-1

def main():

  fname = 'input.txt'

  with open(fname, 'r') as f:
    diskmap = f.readline().strip()

  file_blocks = np.array([int(i) for i in diskmap[::2]])
  spaces      = np.array([int(i) for i in diskmap[1::2]])

  total_space = file_blocks.sum() + spaces.sum()
  full_disk = np.empty((total_space,), dtype=int)
  full_disk.fill(BLANK)

  explode_diskmap(file_blocks, spaces, full_disk)
  rev = full_disk[::-1] # I hope this is just a view :)

  # Find the pivot point
  pivot = np.nonzero(np.cumsum((full_disk==BLANK))==np.cumsum(~(rev==BLANK))[::-1])[0][0]
  nmoves = np.cumsum((full_disk==BLANK))[pivot]

  full_disk[np.nonzero((full_disk==BLANK))[0][:nmoves]] = rev[np.nonzero(~(rev==BLANK))[0][:nmoves]]
  full_disk[pivot:] = BLANK

  checksum = (full_disk[:pivot]*np.arange(pivot)).sum()

  print("Part 1: ", checksum)

if __name__ == '__main__':
  main()
