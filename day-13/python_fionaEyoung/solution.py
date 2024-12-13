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

## Part 2

# Modify Ps
for m in machines:
    m['P'] += 10000000000000

def solve_claw(A, B, P):
    # Linear equations baby
    n_B = ( P[1]*A[0] - P[0]*A[1] ) / ( B[1]*A[0] - B[0]*A[1] )
    n_A = ( P[0] - n_B*B[0]) / A[0]
    if not bool(n_B % 1) and not bool(n_A % 1):
        return int(n_A), int(n_B)
    else:
        return 0, 0

total = 0
for m in machines:
    n_A, n_B = solve_claw(m['A'], m['B'], m['P'])
    total += n_B*cost_B + n_A*cost_A

if fname=='test.txt':
    assert total==875318608908

print("Part 1: ", total)
