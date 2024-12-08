import numpy as np
from itertools import combinations

def find_antinodes(map, result, result_with_harmonics):
  global FLAG
  antennas = np.argwhere(map)

  for a, b in combinations(antennas, 2):
    dir = b - a
    min_harmonic = max(a//abs(dir))
    max_harmonic = max((map.shape-a)//abs(dir))
    for harmonic in range(-min_harmonic, max_harmonic+1):
      pos = a + harmonic*(b-a)
      if any(pos<0): continue
      try:
        if harmonic in (-1, 2): # Part 1 only
          result[tuple(pos)] = True
        result_with_harmonics[tuple(pos)] = True
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
  antinodes_with_harmonics = np.zeros(char_map.shape, dtype=bool)

  for i, f in enumerate(freqs):
    if f == '.': continue
    find_antinodes(int_map==i, antinodes, antinodes_with_harmonics)

  print("Part 1: ", antinodes.sum())
  print("Part 2: ", antinodes_with_harmonics.sum())

if __name__ == '__main__':
  main()
