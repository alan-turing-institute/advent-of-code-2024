use std::env;
use std::fs;
use std::collections::HashSet;

#[derive(Clone, Eq, Hash, PartialEq, Debug)]
struct Position {
    row: usize,
    col: usize,
}

fn get_neighbors(map: &Vec<Vec<char>>, pos: &Position) -> Vec<Position> {
    let mut neighbors = Vec::new();
    let rows = map.len();
    let cols = map[0].len();

    let directions = [(0, 1), (1, 0), (0, -1), (-1, 0)];

    for (dr, dc) in directions.iter() {
        let new_row = pos.row as i32 + dr;
        let new_col = pos.col as i32 + dc;

        if new_row >= 0 && new_row < rows as i32 &&
           new_col >= 0 && new_col < cols as i32 {
            neighbors.push(Position {
                row: new_row as usize,
                col: new_col as usize,
            });
        }
    }

    neighbors
}

// Part 1: Count reachable 9s
fn explore_trail(
    map: &Vec<Vec<char>>,
    current: &Position,
    current_value: char,
    visited: &mut HashSet<Position>,
    nines: &mut HashSet<Position>
) {
    if map[current.row][current.col] == '9' {
        nines.insert(current.clone());
    }

    let next_value = (current_value as u8 + 1) as char;

    for next_pos in get_neighbors(map, current) {
        if map[next_pos.row][next_pos.col] == next_value && !visited.contains(&next_pos) {
            visited.insert(next_pos.clone());
            explore_trail(map, &next_pos, next_value, visited, nines);
            visited.remove(&next_pos);
        }
    }
}

fn part_one(map: &Vec<Vec<char>>) -> i32 {
    let mut total_nines = 0;

    for row in 0..map.len() {
        for col in 0..map[0].len() {
            if map[row][col] == '0' {
                let start_pos = Position { row, col };
                let mut visited = HashSet::new();
                let mut nines = HashSet::new();
                visited.insert(start_pos.clone());

                explore_trail(map, &start_pos, '0', &mut visited, &mut nines);

                total_nines += nines.len();
            }
        }
    }

    total_nines as i32
}

// Part 2: Count unique paths to 9

fn explore_unique_paths(
    map: &Vec<Vec<char>>,
    current: &Position,
    current_value: char,
    path: &mut Vec<Position>,
    all_paths: &mut HashSet<Vec<Position>>
) {
    path.push(current.clone());

    if current_value == '9' {
        all_paths.insert(path.clone());
    } else {
        // Continue exploring if we haven't reached 9
        let next_value = (current_value as u8 + 1) as char;
        for next_pos in get_neighbors(map, current) {
            if map[next_pos.row][next_pos.col] == next_value && !path.contains(&next_pos) {
                explore_unique_paths(map, &next_pos, next_value, path, all_paths);
            }
        }
    }

    path.pop();
}

fn print_map(map: &Vec<Vec<char>>) {
    println!("Map:");
    for row in map {
        for &c in row {
            print!("{}", c);
        }
        println!();
    }
    println!();
}

fn find_trailheads(map: &Vec<Vec<char>>) -> Vec<Position> {
    let mut trailheads = Vec::new();
    for row in 0..map.len() {
        for col in 0..map[0].len() {
            if map[row][col] == '0' {
                trailheads.push(Position { row, col });
            }
        }
    }
    trailheads.sort_by_key(|pos| (pos.row, pos.col));
    trailheads
}

fn part_two(map: &Vec<Vec<char>>) -> i32 {
    let mut total_paths = 0;
    let trailheads = find_trailheads(map);

    for (_, start_pos) in trailheads.iter().enumerate() {
        let mut current_path = Vec::new();
        let mut all_paths = HashSet::new();

        explore_unique_paths(map, start_pos, '0', &mut current_path, &mut all_paths);
        total_paths += all_paths.len();
    }

    total_paths as i32
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let file_path = &args[1];
    println!("Using file {file_path}");

    let contents = fs::read_to_string(file_path)
        .expect("Should have been able to read the file");

    let mut map: Vec<Vec<char>> = Vec::new();
    for line in contents.lines() {
        let mut row: Vec<char> = Vec::new();
        for c in line.chars() {
            row.push(c);
        }
        map.push(row);
    }

    println!("Input map:");
    print_map(&map);

    println!("Part one: {}", part_one(&map));
    println!("Part two: {}", part_two(&map));
}