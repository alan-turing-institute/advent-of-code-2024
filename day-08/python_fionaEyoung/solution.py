import numpy as np
from itertools import combinations

def find_antinodes(map, result):
  global FLAG
  antennas = np.argwhere(map)

  for a, b in combinations(antennas, 2):
    for pos in [2*b - a, 2*a - b]:
      if any(pos<0): continue
      try:
        result[tuple(pos)] = True
      except IndexError:
        continue

def main():

  fname = 'input.txt'

  with open(fname, 'r') as f:
    lines = f.readlines()

  char_map = np.array([[char for char in line.strip()] for line in lines])

  freqs, int_map = np.unique(char_map, return_inverse=True)
  int_map = np.reshape(int_map, char_map.shape)

  antinodes = np.zeros(char_map.shape, dtype=bool)

  for i, f in enumerate(freqs):
    if f == '.': continue
    find_antinodes(int_map==i, antinodes)

  print("Part 1: ", antinodes.sum())

if __name__ == '__main__':
  main()
