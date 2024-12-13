import numpy as np
import re

fname = 'input.txt'

machines = []

with open(fname, 'r') as f:
  line = f.readline()
  while line:
    m = {}
    m['A'] = np.array([int(i) for i in re.findall(r'\d+', line)] )
    m['B'] = np.array([int(i) for i in re.findall(r'\d+', f.readline())] )
    m['P'] = np.array([int(i) for i in re.findall(r'\d+', f.readline())] )
    machines.append(m)
    f.readline()
    line = f.readline()

cost_A = 3
cost_B = 1

total_cost = 0
for m in machines:
  for n_A in range(100):
    claw = m['A']*n_A
    if not ((m['P']-claw)%m['B']).any():
      n_B = ((m['P']-claw)//m['B'])
      if n_B[0]==n_B[1]:
        total_cost += n_B[0]*cost_B + n_A*cost_A
        break

print("Part 1: ", total_cost)
