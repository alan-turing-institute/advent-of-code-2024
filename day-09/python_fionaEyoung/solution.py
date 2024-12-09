import numpy as np

BLANK = -1 # not np.nan, otherwise have to use floats everywhere

def explode_diskmap(files, spaces, result):

  fp, sp = [], [] # pointers

  idx = 0
  for i, (f, s) in enumerate(zip(files, spaces)):

    fp.append((idx, f))
    sp.append((idx+f, s))

    result[idx:idx+f] = i
    idx += f+s
  # end
  result[idx:idx+files[-1]] = len(files)-1

  return fp, sp

def get_spaces(disk_map):
  spaces = np.argwhere(np.diff(disk_map == BLANK ,prepend=False,append=False))
  spaces = spaces.reshape(len(spaces)//2, 2)
  return list(zip( spaces[:,0], np.diff(spaces, axis=1).flat ))

def main():

  fname = 'test.txt'

  with open(fname, 'r') as f:
    diskmap = f.readline().strip()

  file_blocks = np.array([int(i) for i in diskmap[::2]])
  spaces      = np.array([int(i) for i in diskmap[1::2]])

  total_space = file_blocks.sum() + spaces.sum()
  full_disk_original = np.empty((total_space,), dtype=int)
  full_disk_original.fill(BLANK)

  filepntrs, spacepntrs = explode_diskmap(file_blocks, spaces, full_disk_original)

  full_disk = full_disk_original.copy()
  rev = full_disk[::-1] # I hope this is just a view :)

  # Find the pivot point
  pivot = np.nonzero(np.cumsum((full_disk==BLANK))==np.cumsum(~(rev==BLANK))[::-1])[0][0]
  nmoves = np.cumsum((full_disk==BLANK))[pivot]

  full_disk[np.nonzero((full_disk==BLANK))[0][:nmoves]] = rev[np.nonzero(~(rev==BLANK))[0][:nmoves]]
  full_disk[pivot:] = BLANK

  checksum = (full_disk[:pivot]*np.arange(pivot)).sum()

  print("Part 1: ", checksum)

  # full_disk_original
  # Part 2
  print(spacepntrs, get_spaces(full_disk_original))
  # for fpntr, fsize in filepntrs:




if __name__ == '__main__':
  main()
