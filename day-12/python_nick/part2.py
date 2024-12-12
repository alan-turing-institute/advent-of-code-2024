import numpy as np

test_data_1 = """AAAA
BBCD
BBCC
EEEC"""

test_data_2 = """EEEEE
EXXXX
EEEEE
EXXXX
EEEEE"""

test_data_3 = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""




def get_input(test_data = None):
    lines = []
    if test_data:
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

def get_sides(region):
    total = 0
    sides = {
        "upper": {"edge_direction": (-1,0),"neighbour_directions": [(0,-1),(0,1)], "sides": []},
        "lower": {"edge_direction": (1,0),"neighbour_directions": [(0,-1),(0,1)], "sides": []},
        "left": {"edge_direction": (0,-1),"neighbour_directions": [(-1,0),(1,0)], "sides": []},
        "right": {"edge_direction": (0,1),"neighbour_directions": [(-1,0),(1,0)], "sides": []},
    }
    # important that we sort the squares in the region, so any contiguous ones are next to each other.
    for square in sorted(region):
        for k, v in sides.items():
            if (square[0]+v["edge_direction"][0], square[1]+v["edge_direction"][1]) not in region:
                # This square is on a side of type v['edge_direction']
                # Look at it's neighbours in the perpendicular direction to see if we already have this side
                new_side = True
                for side in v["sides"]:
                    for direction in v["neighbour_directions"]:
                        if (square[0]+direction[0], square[1]+direction[1]) in side:
                            # we already have the side - extend it with this new square
                            side.add(square)
                            new_side = False
                            break
                if new_side:
                    # we didn't already have the side - add a new set to the "sides" list
                    v["sides"].append(set([square]))
    # return the whole dict, to help debugging
    return sides

def count_sides(sides):
    """
    Get the number of sides from the sides dict returned by get_sides.
    """
    total = 0
    for v in sides.values():
        total += len(v["sides"])
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


garden = get_input()
regions = get_all_regions(garden)
total = 0
for region in regions:
    sides = get_sides(region)
    total += get_area(region) * count_sides(sides)


print(f"Part 2: {total}")
