"""
Advent of Code 2024
Day 08
tomogwen
"""
from itertools import combinations
from pathlib import Path


def parse_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    map = [list(line.strip()) for line in lines]

    return map


def process_map(map):
    """Returns a dict with keys unique antenna and values lists of locations."""
    antennae = {}
    for i, row in enumerate(map):
        for j, element in enumerate(row):
            if element != '.':
                if element not in antennae.keys():
                    antennae[element] = [[i, j]]
                else:
                    antennae[element].append([i, j])
    return antennae


def part_one(antennae):
    nodes0 = []
    for antenna in antennae.keys():
        for pairs in combinations(antennae[antenna], 2):
            i_dist = pairs[0][0] - pairs[1][0]
            j_dist = pairs[0][1] - pairs[1][1]

            potential_nodes = [[pairs[0][0] + i_dist, pairs[0][1] + j_dist],
                               [pairs[1][0] - i_dist, pairs[1][1] - j_dist]]

            for node in potential_nodes:
                if 0 <= node[0] < len(map) and 0 <= node[1] < len(map[0]):
                    if node not in nodes0:
                        nodes0.append(node)
    
    return nodes0


def part_two(antennae):
    nodes1 = []
    for antenna in antennae.keys():
        for pairs in combinations(antennae[antenna], 2):
            i_dist = pairs[0][0] - pairs[1][0]
            j_dist = pairs[0][1] - pairs[1][1]  

            directions = [[i_dist, j_dist], [-i_dist, -j_dist]]
            for node, direction in zip(pairs, directions):                
                while 0 <= node[0] < len(map) and 0 <= node[1] < len(map[0]):
                    if node not in nodes1:
                        nodes1.append(node)
                    node = [node[0] + direction[0], node[1] + direction[1]]
    return nodes1


if __name__ == "__main__":
    file_path = Path("input.txt")
    map = parse_file(file_path)
    antennae = process_map(map)

    nodes0 = part_one(antennae)
    nodes1 = part_two(antennae)    

    print("Part 1 solution:", len(nodes0))
    print("Part 2 solution:", len(nodes1))
