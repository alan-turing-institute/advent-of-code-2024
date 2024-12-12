use std::collections::HashMap;
use crate::Region;

pub fn print_coloured_map(map: &[Vec<char>], regions: &[Region]) {
    println!("\nColoured map:");

    let colours = [
        "\x1b[31m", "\x1b[32m", "\x1b[34m", "\x1b[33m",
        "\x1b[35m", "\x1b[36m", "\x1b[91m", "\x1b[92m",
        "\x1b[94m", "\x1b[93m", "\x1b[95m", "\x1b[96m",
    ];
    let reset = "\x1b[0m";

    let region_colours = assign_region_colours(regions, colours.len());
    let pos_to_colour = create_colour_map(regions, &region_colours, &colours);

    // Print the coloured map
    for y in 0..map.len() {
        for x in 0..map[0].len() {
            let colour = pos_to_colour.get(&(x, y)).unwrap_or(&reset);
            print!("{}{}{}", colour, map[y][x], reset);
        }
        println!();
    }
    println!();
}

fn assign_region_colours(regions: &[Region], num_colours: usize) -> HashMap<usize, usize> {
    let adjacencies = build_adjacency_map(regions);
    let mut region_colours = HashMap::new();

    for region_idx in 0..regions.len() {
        let mut used_colours = vec![false; num_colours];

        if let Some(adjacent) = adjacencies.get(&region_idx) {
            for &adj_idx in adjacent {
                if let Some(&colour) = region_colours.get(&adj_idx) {
                    used_colours[colour] = true;
                }
            }
        }

        let colour = used_colours.iter()
            .position(|&used| !used)
            .unwrap_or(0);
        region_colours.insert(region_idx, colour);
    }

    region_colours
}

fn build_adjacency_map(regions: &[Region]) -> HashMap<usize, Vec<usize>> {
    let mut adjacencies: HashMap<usize, Vec<usize>> = HashMap::new();

    for (i, region1) in regions.iter().enumerate() {
        for (j, region2) in regions.iter().enumerate() {
            if i != j && regions_are_adjacent(region1, region2) {
                adjacencies.entry(i).or_default().push(j);
            }
        }
    }

    adjacencies
}

fn regions_are_adjacent(region1: &Region, region2: &Region) -> bool {
    for plot1 in &region1.plots {
        for plot2 in &region2.plots {
            if (plot1.x as i32 - plot2.x as i32).abs() +
               (plot1.y as i32 - plot2.y as i32).abs() == 1 {
                return true;
            }
        }
    }
    false
}

fn create_colour_map<'a>(
    regions: &[Region],
    region_colours: &HashMap<usize, usize>,
    colours: &'a [&str]
) -> HashMap<(usize, usize), &'a str> {
    let mut pos_to_colour = HashMap::new();

    for (region_idx, region) in regions.iter().enumerate() {
        let colour_idx = region_colours[&region_idx];
        for plot in &region.plots {
            pos_to_colour.insert((plot.x, plot.y), colours[colour_idx]);
        }
    }

    pos_to_colour
}