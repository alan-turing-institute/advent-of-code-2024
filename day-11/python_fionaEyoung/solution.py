import numpy as np
from tqdm import tqdm
from multiprocessing import Pool, cpu_count
from contextlib import closing
from itertools import repeat
from functools import cache

def n_digits(num):
    return np.log10(num).astype(int)+1

@cache
def split_num(num):
    s = str(num)
    return ( int(s[:len(s)//2]), int(s[len(s)//2:]) )

def split_stones(stones, indices):
    arrs = np.split(stones, indices)
    for i in range(len(arrs)-1):
        nums = split_num(arrs[i][-1])
        arrs[i][-1] = nums[0]
        arrs[i] = np.append(arrs[i], nums[1])

    return np.concatenate(arrs)

def blink(stones):
    # stones = [s1, s2, ...]
    changed = np.zeros(stones.shape, dtype=bool)

    # Rule 1
    changed |= stones==0
    stones[stones==0] = 1

    # Rule 2
    splits = ~(n_digits(stones)%2).astype(bool)
    changed |= splits

    # Rule 3
    stones[~changed] *= 2024

    # Only now apply rule 2
    return split_stones(stones, np.flatnonzero(splits)+1)

@cache
def sblink(stone):
    if stone==0: return (1,)
    if not int(n_digits(stone)%2): return split_num(stone)
    return (stone*2024,)


def blink_loop(arr, n):
    for b in tqdm(range(n)):
    # for b in range(n):
        arr = blink(arr)
    return arr

def main():
    fname = 'input.txt'

    with open(fname, 'r') as f:
      stones = np.array([int(s) for s in f.readline().strip().split()])

    n_blinks_p1 = 25#25 # 25
    n_blinks_p2 = 75 - n_blinks_p1 #75-n_blinks_p1 # 75

    lens = []

    for b in range(n_blinks_p1):
        stones = blink(stones)
        lens.append(len(stones))

    print("Part 1: ", len(stones))

    ## Part 2: Ignore the sequence, store only the unique values and how many of them there are

    map = {}
    counts = {}

    for s in stones:
        if s in counts: counts[s] += 1
        else: counts[s] = 1

    for _ in range(n_blinks_p2):

        new_counts = {}

        for s, n in counts.items():

            if s in map:
                new_stone_s = map[s]
            else:
                new_stone_s = sblink(s)
                map[s] = new_stone_s

            for new_s in new_stone_s:
                if new_s in new_counts:
                    new_counts[new_s] += n
                else: new_counts[new_s] = n

        counts = new_counts

    print("Part 2: ", sum(new_counts.values()))

if __name__ == '__main__':
    main()
