// use std::env;
// use std::fs;


// fn main() {
//     // Read input file
//     let args: Vec<String> = env::args().collect();
//     let file_path = &args[1];
//     println!("Using file {file_path}");

//     let contents = fs::read_to_string(file_path)
//         .expect("Should have been able to read the file");

//     // Parse the disk map
//     let blocks = parse_disk_map(contents.trim());

//     // Convert to individual blocks
//     let mut individual_blocks = expand_to_individual_blocks(&blocks);

//     // Compact the disk
//     compact_disk(&mut individual_blocks);

//     // Calculate and print checksum
//     let checksum = calculate_checksum(&individual_blocks);
//     println!("Part one (Filesystem checksum): {}", checksum);
// }


// #[derive(Debug)]
// struct Block {
//     file_id: Option<usize>,
//     size: usize,
// }

// fn parse_disk_map(input: &str) -> Vec<Block> {
//     let numbers: Vec<usize> = input.chars()
//         .map(|c| c.to_digit(10).unwrap() as usize)
//         .collect();

//     let mut blocks = Vec::new();
//     let mut file_id = 0;

//     // Convert alternating numbers into blocks with file IDs
//     for (i, &size) in numbers.iter().enumerate() {
//         if i % 2 == 0 {
//             // File block
//             blocks.push(Block {
//                 file_id: Some(file_id),
//                 size,
//             });
//             file_id += 1;
//         } else {
//             // Free space block
//             blocks.push(Block {
//                 file_id: None,
//                 size,
//             });
//         }
//     }

//     blocks
// }

// fn expand_to_individual_blocks(blocks: &[Block]) -> Vec<Option<usize>> {
//     let mut result = Vec::new();

//     for block in blocks {
//         for _ in 0..block.size {
//             result.push(block.file_id);
//         }
//     }

//     result
// }

// fn compact_disk(blocks: &mut Vec<Option<usize>>) {
//     let len = blocks.len();
//     for i in (0..len).rev() {
//         if blocks[i].is_some() {
//             // Find leftmost free space
//             for j in 0..i {
//                 if blocks[j].is_none() {
//                     // Move the file block
//                     blocks[j] = blocks[i];
//                     blocks[i] = None;
//                     break;
//                 }
//             }
//         }
//     }
// }

// fn calculate_checksum(blocks: &[Option<usize>]) -> usize {
//     blocks.iter()
//         .enumerate()
//         .filter_map(|(pos, &file_id)| {
//             file_id.map(|id| pos * id)
//         })
//         .sum()
// }



// #[cfg(test)]
// mod tests {
//     use super::*;

//     #[test]
//     fn test_example() {
//         let input = "12345";
//         let blocks = parse_disk_map(input);
//         let mut individual_blocks = expand_to_individual_blocks(&blocks);
//         compact_disk(&mut individual_blocks);

//         // Check final state (should be "022111222......")
//         let expected: Vec<Option<usize>> = vec![
//             Some(0), Some(2), Some(2), Some(1), Some(1), Some(1),
//             Some(2), Some(2), Some(2), None, None, None, None, None, None
//         ];
//         assert_eq!(individual_blocks, expected);
//     }

//     #[test]
//     fn test_checksum() {
//         let input = "2333133121414131402";
//         let blocks = parse_disk_map(input);
//         let mut individual_blocks = expand_to_individual_blocks(&blocks);
//         compact_disk(&mut individual_blocks);
//         let checksum = calculate_checksum(&individual_blocks);

//         // checksum should be 1928
//         let expected = 1928;

//         assert_eq!(checksum, expected);
//     }
// }

use std::env;
use std::fs;

#[derive(Debug)]
struct Block {
    file_id: Option<usize>,
    size: usize,
}

fn parse_disk_map(input: &str) -> Vec<Block> {
    let numbers: Vec<usize> = input.chars()
        .map(|c| c.to_digit(10).unwrap() as usize)
        .collect();

    let mut blocks = Vec::new();
    let mut file_id = 0;

    for (i, &size) in numbers.iter().enumerate() {
        if i % 2 == 0 {
            blocks.push(Block {
                file_id: Some(file_id),
                size,
            });
            file_id += 1;
        } else {
            blocks.push(Block {
                file_id: None,
                size,
            });
        }
    }

    blocks
}

fn expand_to_individual_blocks(blocks: &[Block]) -> Vec<Option<usize>> {
    let mut result = Vec::new();

    for block in blocks {
        for _ in 0..block.size {
            result.push(block.file_id);
        }
    }

    result
}

// Part 1: Move individual blocks
fn compact_disk_blocks(blocks: &mut Vec<Option<usize>>) {
    let len = blocks.len();
    for i in (0..len).rev() {
        if blocks[i].is_some() {
            // Find leftmost free space
            for j in 0..i {
                if blocks[j].is_none() {
                    // Move the file block
                    blocks[j] = blocks[i];
                    blocks[i] = None;
                    break;
                }
            }
        }
    }
}

// Part 2: Move whole files
fn find_file_bounds(blocks: &[Option<usize>], file_id: usize) -> Option<(usize, usize)> {
    let start = blocks.iter().position(|&b| b == Some(file_id))?;
    let end = blocks.iter()
        .skip(start)
        .position(|&b| b != Some(file_id))
        .map_or(blocks.len(), |p| p + start);
    Some((start, end))
}

fn find_leftmost_space(blocks: &[Option<usize>], required_size: usize) -> Option<usize> {
    let mut current_size = 0;
    let mut start_pos = 0;

    for (i, &block) in blocks.iter().enumerate() {
        if block.is_none() {
            if current_size == 0 {
                start_pos = i;
            }
            current_size += 1;
            if current_size >= required_size {
                return Some(start_pos);
            }
        } else {
            current_size = 0;
        }
    }
    None
}

fn compact_disk_whole_files(blocks: &mut Vec<Option<usize>>) {
    let max_file_id = blocks.iter()
        .filter_map(|&x| x)
        .max()
        .unwrap_or(0);

    // Process files in decreasing order of file ID
    for file_id in (0..=max_file_id).rev() {
        // Find current file bounds
        if let Some((start, end)) = find_file_bounds(blocks, file_id) {
            let file_size = end - start;

            // Find leftmost space that can fit the file
            if let Some(new_pos) = find_leftmost_space(&blocks[..start], file_size) {
                // Move the whole file
                let file_blocks: Vec<_> = blocks[start..end].to_vec();
                for i in new_pos..(new_pos + file_size) {
                    blocks[i] = file_blocks[i - new_pos];
                }
                for i in start..end {
                    blocks[i] = None;
                }
            }
        }
    }
}

fn calculate_checksum(blocks: &[Option<usize>]) -> usize {
    blocks.iter()
        .enumerate()
        .filter_map(|(pos, &file_id)| {
            file_id.map(|id| pos * id)
        })
        .sum()
}

fn solve_part1(input: &str) -> usize {
    let blocks = parse_disk_map(input.trim());
    let mut individual_blocks = expand_to_individual_blocks(&blocks);
    compact_disk_blocks(&mut individual_blocks);
    calculate_checksum(&individual_blocks)
}

fn solve_part2(input: &str) -> usize {
    let blocks = parse_disk_map(input.trim());
    let mut individual_blocks = expand_to_individual_blocks(&blocks);
    compact_disk_whole_files(&mut individual_blocks);
    calculate_checksum(&individual_blocks)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let file_path = &args[1];
    println!("Using file {file_path}");

    let contents = fs::read_to_string(file_path)
        .expect("Should have been able to read the file");

    let part1_solution = solve_part1(&contents);
    let part2_solution = solve_part2(&contents);

    println!("Part 1 solution: {}", part1_solution);
    println!("Part 2 solution: {}", part2_solution);
}