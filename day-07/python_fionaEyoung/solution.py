from operator import add, mul
from itertools import product, chain, zip_longest
from functools import reduce, partial
from tqdm import tqdm

def concat(x, y):
  return int(str(x)+str(y))

def operation_reduce(x, y):
  #https://stackoverflow.com/a/70227259
  if callable(x):
      return x(y)
  else:
      return partial(y, x)

def test_eqn(result, operands, operators):
  nops = len(operands)-1

  for ops in product(operators, repeat=nops):
    funciter = [x for x in chain(*zip_longest(operands, ops)) if x is not None]
    if reduce(operation_reduce, funciter) == result:
      return True

  return False

def main():

  fname = 'input.txt'

  with open(fname, 'r') as f:
    eqns = f.readlines()

  OPERATORS1 = (add, mul)
  OPERATORS2 = (add, mul, concat)

  total1 = 0
  total2_extra = 0

  for eqn in tqdm(eqns):

    result, operands = eqn.split(':')
    operands = [int(o) for o in operands.strip().split()]
    result = int(result)

    if test_eqn(result, operands, OPERATORS1):
      total1 += result
    elif test_eqn(result, operands, OPERATORS2):
      total2_extra += result

  print("Part 1: ", total1)
  print("Part 2: ", total1+total2_extra)

if __name__ == '__main__':
  main()
