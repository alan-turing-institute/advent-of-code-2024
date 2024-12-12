import numpy as np

test_data = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""

def get_input(test=True):
    lines = []
    if test:
        for line in test_data.split("\n"):
            lines.append(list(line.strip()))
    else:
        for line in open("input.txt").readlines():
            lines.append(list(line.strip()))
    return np.array(lines)



def get_neighbours(x,y, garden, neighbours):
    neighbours.add((x,y))
    value = garden[x,y]
    directions = [(-1,0),(1,0),(0,-1),(0,1)]
    for direction in directions:
        new_x = x+direction[0]
        new_y = y+direction[1]
        if new_x not in range(0, garden.shape[0]) or new_y not in range(0, garden.shape[1]):
            continue
        if (new_x, new_y) in neighbours:
            continue
        if garden[new_x, new_y] == value:
           neighbours =  neighbours.union(get_neighbours(new_x, new_y, garden, neighbours))
    return neighbours


def get_area(region):
    return len(region)

def get_perimeter(region):
    total = 0
    for square in region:
        sides = 4
        for direction in [(-1,0),(1,0),(0,-1),(0,1)]:
            if (square[0]+direction[0],square[1]+direction[1]) in region:
                sides -= 1
        total += sides
    return total


def get_all_regions(garden):
    regions = []
    for ix in range(garden.shape[0]):
        for iy in range(garden.shape[1]):
            # check if already in a region
            already_in_region = False
            for r in regions:
                if (ix, iy) in r:
                    already_in_region = True
                    break
            if already_in_region:
                continue
            regions.append(get_neighbours(ix, iy, garden, set([])))
    return regions


garden = get_input(False)
regions = get_all_regions(garden)
total = 0
for region in regions:
    total += get_area(region) * get_perimeter(region)


print(f"Part 1: {total}")
