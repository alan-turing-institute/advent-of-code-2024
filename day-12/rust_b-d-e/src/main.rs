mod mapcolour;

use std::env;
use std::fs;
use std::collections::HashSet;
use std::fmt;

fn main() {
    let args: Vec<String> = env::args().collect();
    let file_path = &args[1];
    println!("Using file {file_path}");

    let contents = fs::read_to_string(file_path)
        .expect("Should have been able to read the file");

    let map = parse_map(&contents);
    let regions = find_regions(&map);  // Changed to take reference

    let mut part_one = 0;
    let mut part_two = 0;

    for region in &regions {
        let area = region.area();
        let perimeter = region.perimeter();
        let num_sides = region.num_sides();

        // println!(
        //     "Region: {}, area: {}, perimeter: {}, num_sides: {}, p1: {}, p2: {}",
        //     region, area, perimeter, num_sides, area * perimeter, area * num_sides
        // );

        part_one += area * perimeter;
        part_two += area * num_sides;
    }

    println!("Part one: {}", part_one);
    println!("Part two: {}", part_two);

    mapcolour::print_coloured_map(&map, &regions);
}


// Data structures
#[derive(Debug, PartialEq, Eq, Hash, Clone)]
struct Plot {
    plant: char,
    x: usize,
    y: usize,
}

impl Plot {
    fn new(x: usize, y: usize, plant: char) -> Self {
        Self { x, y, plant }
    }

    // Get coordinates of a neighbor in a given direction
    fn neighbor_coords(&self, dx: i32, dy: i32) -> Option<(usize, usize)> {
        let new_x = self.x as i32 + dx;
        let new_y = self.y as i32 + dy;

        if new_x >= 0 && new_y >= 0 {
            Some((new_x as usize, new_y as usize))
        } else {
            None
        }
    }
}

#[derive(Clone)]
struct Region {
    plots: HashSet<Plot>,
}

impl fmt::Display for Region {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        if self.plots.is_empty() {
            write!(f, "empty")
        } else {
            write!(f, "{}", self.plots.iter().next().unwrap().plant)
        }
    }
}

impl Region {
    fn new(plots: HashSet<Plot>) -> Self {
        Self { plots }
    }

    fn area(&self) -> i32 {
        self.plots.len() as i32
    }

    fn has_neighbor(&self, plot: &Plot, dx: i32, dy: i32) -> bool {
        if let Some((x, y)) = plot.neighbor_coords(dx, dy) {
            self.plots.contains(&Plot::new(x, y, plot.plant))
        } else {
            false
        }
    }

    fn perimeter(&self) -> i32 {
        let directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]; // N, E, S, W
        let mut perimeter = 0;

        for plot in &self.plots {
            for &(dx, dy) in &directions {
                if !self.has_neighbor(plot, dx, dy) {
                    perimeter += 1;
                }
            }
        }
        perimeter
    }

    fn num_sides(&self) -> i32 {
        let mut sides = 0;

        for plot in &self.plots {
            // Get all neighbor states in a consistent order
            let n = self.has_neighbor(plot, 0, -1);
            let e = self.has_neighbor(plot, 1, 0);
            let s = self.has_neighbor(plot, 0, 1);
            let w = self.has_neighbor(plot, -1, 0);
            let ne = self.has_neighbor(plot, 1, -1);
            let se = self.has_neighbor(plot, 1, 1);
            let sw = self.has_neighbor(plot, -1, 1);
            let nw = self.has_neighbor(plot, -1, -1);

            // External corners
            for &(n1, n2) in &[(n, e), (e, s), (s, w), (w, n)] {
                if !n1 && !n2 { sides += 1; }
            }

            // Internal corners
            for &(straight1, straight2, diag) in &[
                (n, e, ne), (e, s, se), (s, w, sw), (w, n, nw)
            ] {
                if straight1 && straight2 && !diag { sides += 1; }
            }
        }
        sides
    }
}

// Parsing functions
fn parse_map(contents: &str) -> Vec<Vec<char>> {
    contents.lines()
        .map(|line| line.chars().collect())
        .collect()
}

fn find_regions(map: &[Vec<char>]) -> Vec<Region> {
    let mut regions = Vec::new();
    let mut visited = HashSet::new();

    for y in 0..map.len() {
        for x in 0..map[0].len() {
            let plot = Plot::new(x, y, map[y][x]);
            if !visited.contains(&plot) {
                regions.push(flood_fill(map, &plot, &mut visited));
            }
        }
    }
    regions
}

fn flood_fill(map: &[Vec<char>], start: &Plot, visited: &mut HashSet<Plot>) -> Region {
    let mut plots = HashSet::new();
    let mut to_visit = vec![start.clone()];

    while let Some(plot) = to_visit.pop() {
        if visited.contains(&plot) {
            continue;
        }

        visited.insert(plot.clone());
        plots.insert(plot.clone());

        // Check orthogonal neighbors
        for &(dx, dy) in &[(0, -1), (1, 0), (0, 1), (-1, 0)] {
            if let Some((x, y)) = plot.neighbor_coords(dx, dy) {
                if y < map.len() && x < map[0].len() && map[y][x] == plot.plant {
                    to_visit.push(Plot::new(x, y, plot.plant));
                }
            }
        }
    }
    Region::new(plots)
}