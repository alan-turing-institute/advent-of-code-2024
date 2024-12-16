import re
import numpy as np
import curses
import time
from itertools import cycle

mode = 'input' # 'input'
fname = f'{mode}.txt'
space = (11,7) if mode=='test' else (101,103)

t = 100 # seconds

robots = []

with open(fname, 'r') as f:
  # line = f.readline()
  for line in f:
    robots.append( [int(i) for i in re.findall('-{0,1}\d+', line)] )

robots = np.array(robots)
ps = robots[:,:2]
vs = robots[:,2:]

new_p = ps
for second in range(t):
  new_p = (new_p + vs) % space

def get_safety():
  map = np.zeros(space)
  for r in ps:
    map[tuple(r)] += 1

  mx, my = np.array(space)//2
  return map[:mx, :my].sum() * map[:mx, my+1:].sum() * map[mx+1:, :my].sum() * map[mx+1:, my+1:].sum()


s_factor = get_safety()

print("Part 1: ", s_factor)

# Part 2

def block_str(arr):
  if not arr.any():
    return ' '
  elif (arr>0).all():
    return '8'
  elif arr[0]:
    return 'º'
  elif arr[1]:
    return 'o'
  return '.'

def update_robots(stdscr, t, move=True):
  global ps
  if move:
    ps = (ps + vs) % space
  map = np.zeros(space)
  for r in ps:
    map[tuple(r)] += 1
  for i in range(0, len(map), 2):
    row = [block_str(x) for x in map[i:i+2, :].T]
    stdscr.addstr(i//2, 0, ''.join(row))
    # print(''.join(row))
    # print(map[i:i+2, :])
  # for y, line in enumerate(map):
    # stdscr.addstr(y, 0, ''.join([' ' if not x else 'o' for x in line]))
    # stdscr.addstr(y, 0, "new string")
  stdscr.addstr(len(map)//4, map.shape[1]+10, f"t={t}s")
  stdscr.refresh()

def reset_robots():
  global ps
  ps = robots[:,:2]

def find_min_safety():
  reset_robots()
  min_s = get_safety()
  min_i = 0
  for i in range(np.prod(space)):
    ff_robots(i)
    s = get_safety()
    if s < min_s:
      min_s = s
      min_i = i
  return min_s, min_i

def main_p2_print():

  reset_robots()
  ff_robots(637)

def ff_robots(t):
  global ps
  for second in range(t):
    ps = (ps + vs) % space

def main_p2(stdscr):
  stdscr.clear()
  curses.noecho()
  curses.cbreak()
  stdscr.nodelay(True)

  reset_robots()

  offset = [33,87]

  # t_start = offset[0] + (np.prod(space)) - 20
  t_start = 630 #10537
  # t_start = offset[0]
  t_end = 195
  n_steps = 1000

  # first horizontal = 33, 134, 235,...;  first vertical = 87, 190, 293, ....
  # 2861

  t_steps =  np.ravel((np.arange(0, n_steps) * space[0] + offset[0],
                       np.arange(0, n_steps) * space[1] + offset[1]), order='F')

  try:
      # ff_robots(80)
      t = t_start
      # for i, step in enumerate(cycle(space)):
      ff_robots(t)
      update_robots(stdscr, t, move=False)
      # for t in range(t_start, t_end):
      # for t_step in np.diff(t_steps):
      for t_step in range(n_steps):
          # t += t_step
          t += 1
          ff_robots(t_step)
          stdscr.nodelay(True)
          update_robots(stdscr, t, move=False)
          time.sleep(.5)
          key = stdscr.getch()
          if key == -1:
            continue
          else:
            stdscr.nodelay(False)
            stdscr.getch()
  finally:
      curses.echo()
      curses.nocbreak()
      curses.endwin()
      print(t)

curses.wrapper(main_p2)
# main_p2_print()

# print(find_min_safety())
