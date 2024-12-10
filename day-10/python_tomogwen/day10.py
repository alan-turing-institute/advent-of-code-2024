"""
Advent of Code 2024
Day 10
tomogwen
"""
from pathlib import Path


def parse_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    map = [[int(x) for x in list(line.strip())] for line in lines]
    return map


def find_trailheads(map):
    theads = []
    for i, row in enumerate(map):
        for j, element in enumerate(row):
            if element == 0:
                theads.append([i, j])
    return theads


def find_routes(location, goal_height, nine_reached, nine_count):
    for direction in [[+1, 0], [-1, 0], [0, +1], [0, -1]]:
        new_location = [location[0]+direction[0], location[1]+direction[1]]
        # check valid coordinate
        if 0 <= new_location[0] < len(map) and 0 <= new_location[1] < len(map[0]):
            # check if we've reached correct height
            if map[new_location[0]][new_location[1]] == goal_height:
                # reached end of trail
                if goal_height == 9:
                    nine_count += 1
                    if new_location not in nine_reached:
                        nine_reached.append(new_location)
                # reached correct height and need to check next
                else:
                    nine_reached, nine_count = find_routes(new_location, goal_height+1, nine_reached, nine_count)
    return nine_reached, nine_count


if __name__ == "__main__":
    file_path = Path("input.txt")
    map = parse_file(file_path)    
    trailheads = find_trailheads(map)

    part_one, part_two = 0, 0
    for head in trailheads:
        nine_reached, nine_count = find_routes(head, goal_height=1, nine_reached=[], nine_count=0)
        part_one += len(nine_reached)
        part_two += nine_count

    print("Part 1 solution:", part_one)
    print("Part 2 solution:", part_two)
