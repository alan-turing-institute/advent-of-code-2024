"""
Advent of Code 2024
Day 05
tomogwen
"""
from pathlib import Path
from tqdm import tqdm


class Guard:
    def __init__(self, map):
        self.map = map
        i, j = self._find_guard()
        self.i = i
        self.j = j
        self.facing = 'up'
        self.path = [[0 for x in range(len(map[0]))] for _ in range(len(map))]
        self.finished = False

    def patrol(self):
        """Returns true if patrol looping, false if patrol escapes"""
        self.path[self.i][self.j] = "up"
        while not self.finished:
            guard._move()
            if self._in_loop() and not self.finished:
                return True
            self.path[self.i][self.j] = self.facing
        return False

    def squares_covered(self):
        count = 0
        for row in self.path:
            for square in row:
                if square != 0:
                    count += 1
        return count

    def _in_loop(self):
        if self.path[self.i][self.j] == self.facing:
            return True
        else:
            return False

    def _move(self):
        match self.facing:
            case 'up':
                next_i = self.i-1
                next_j = self.j
            case 'right':
                next_i = self.i
                next_j = self.j+1
            case 'down':
                next_i = self.i+1
                next_j = self.j
            case 'left':
                next_i = self.i
                next_j = self.j-1
            
        if next_i < 0 or len(map) <= next_i or next_j < 0 or len(map[0]) <= next_j:
            self.finished = True
        elif self.map[next_i][next_j] == '#':
            self._rotate()
            self._move()
        else:
            self.i = next_i
            self.j = next_j
    
    def _rotate(self):
        match self.facing:
            case 'up':
                self.facing = 'right'
            case 'right':
                self.facing = 'down'
            case 'down':
                self.facing = 'left'
            case 'left':
                self.facing = 'up'
            
    def _find_guard(self):
        for i, row in enumerate(self.map):
            for j, entry in enumerate(row):
                if entry == '^':
                    return i, j



def parse_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    map = [list(line.strip()) for line in lines]

    return map


if __name__ == "__main__":
    file_path = Path("input.txt")
    map = parse_file(file_path)

    guard = Guard(map)
    _ = guard.patrol()
    part_one = guard.squares_covered()
    print("Part 1 solution:", part_one)

    part_two = 0
    for i, row in tqdm(enumerate(map)):
        for j, element in enumerate(row):
            if element != '#' and element != '^':
                map[i][j] = '#'
                guard = Guard(map)
                looping = guard.patrol()
                map[i][j] = '.'
                if looping:
                    part_two += 1
    print("Part 2 solution:", part_two)
