import numpy as np

BLANK = -1 # not np.nan, otherwise have to use floats everywhere

def explode_diskmap(files, spaces, result):
  fp, sp = [], [] # pointers

  idx = 0
  for i, (f, s) in enumerate(zip(files, spaces)):

    fp.append((idx, f))
    if s: sp.append((idx+f, s))

    result[idx:idx+f] = i
    idx += f+s
  # end
  fp.append((idx, files[-1]))
  result[idx:idx+files[-1]] = len(files)-1

  return fp, sp

def get_spaces(disk_map):
  spaces = np.argwhere(np.diff(disk_map == BLANK ,prepend=False,append=False))
  spaces = spaces.reshape(len(spaces)//2, 2)
  return list(zip( spaces[:,0], np.diff(spaces, axis=1).flat ))

#%%
fname = 'input.txt'

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

files = {id:{'idx':idx, 'size':size} for id, (idx, size) in enumerate(filepntrs)}

# Try and move each file exactly once
for fid in range(max(full_disk_original), -1, -1):
    # Get the size of this file block
    fsize = files[fid]['size']
    # Check for any space pointers where
    # 1. The pointer index is less than the files'
    # 2. The space is big enough
    for i in range(len(spacepntrs)):
        space = spacepntrs[i]
        if (space[0] < files[fid]['idx']) and (space[1] >= fsize):

            files[fid]['idx'] = space[0]

            # replace the space pointer: it either got smaller or disappeared
            new_spntr = (space[0]+fsize, space[1]-fsize)

            # Modify the list of spacepntrs
            if space[1]==fsize:
                spacepntrs.remove(space)
            else:
                spacepntrs[i] = new_spntr
            # only move for the first matching space!
            break

checksum = sum( sum(fid*loc for loc in range(f['idx'], f['idx']+f['size'])) for fid, f in files.items() )

print("Part 2: ", checksum)
