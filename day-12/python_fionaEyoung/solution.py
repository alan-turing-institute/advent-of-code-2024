import numpy as np
from skimage.measure import regionprops, label
from scipy.ndimage import convolve


fname = 'input.txt'
with open(fname, 'r') as f:
    lines = f.readlines()

map = np.array([[ord(char) for char in line.strip()] for line in lines])
lmap = label(map, connectivity=1)

regions = regionprops(lmap)

neighbour_filter = [[ 0,-1, 0],
                    [-1, 4,-1],
                    [ 0,-1, 0]]

price = 0
for r in regions:
     a = convolve((lmap==r.label).astype(int), weights=neighbour_filter, mode='constant', cval=0)
     area = int(r.area)
     contour = int(a[a>0].sum())
     # id = chr(map[lmap==r.label][0])
     price += area*contour

print("Part 1: ", price)
