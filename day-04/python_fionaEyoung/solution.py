import numpy as np
import re

def detect_xmas(b):
  assert b.shape == (3,3)

  if not b[1,1] == 'A': return False

  corners = b[::2, ::2]

  if all(corners[0]=='M') and all(corners[1]=='S'): return True
  if all(corners[0]=='S') and all(corners[1]=='M'): return True
  if (corners[0]==['M', 'S']).all() and (corners[1]==['M', 'S']).all() : return True
  if (corners[0]==['S', 'M']).all() and (corners[1]==['S', 'M']).all() : return True

  return False

def main():

  fname = 'input.txt'

  with open(fname, 'r') as file:
    lines = file.readlines()

  wordsearch = np.array([[char for char in line.strip()] for line in lines])

  # print(np.diagonal(wordsearch, offset=1))
  pattern = 'XMAS'
  max_offset = wordsearch.shape[0]-len(pattern)

  flippedlr = np.fliplr(wordsearch)
  flippedud = np.flipud(wordsearch)

  diagonals     = [ ''.join(np.diagonal(wordsearch, offset=i)) for i in range(-max_offset, max_offset+1) ]
  antidiagonals = [ ''.join(np.diagonal(flippedlr, offset=i)) for i in range(-max_offset, max_offset+1) ]

  diagonals += [ diag[::-1] for diag in diagonals ]
  antidiagonals += [ diag[::-1] for diag in antidiagonals ]

  rows = [ ''.join(row) for row in wordsearch ] + [ ''.join(row) for row in flippedlr ]
  cols = [ ''.join(col) for col in wordsearch.T ] + [ ''.join(col) for col in flippedud.T ]

  total = sum( len(re.findall(pattern, _string)) for _string in
    diagonals + antidiagonals + rows + cols
  )

  print("Part 1: ", total)

  # Part 2

  total = 0

  a_i, a_j = np.nonzero(wordsearch == 'A')

  for i, j in zip(a_i, a_j):

    # why is this so ugly
    if i==0 or i==wordsearch.shape[0]-1 or j==0 or j==wordsearch.shape[1]-1: continue

    block = wordsearch[i-1:i+2, j-1:j+2]

    total += detect_xmas(block)

  print("Part 2: ", total)


if __name__ == '__main__':
  main()
