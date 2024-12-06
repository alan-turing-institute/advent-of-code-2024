use std::env;
use std::fs;
use std::collections::{HashMap, HashSet};
use std::cmp::Ordering;

fn main() {
    // read in the file

    let args: Vec<String> = env::args().collect();

    let file_path = &args[1];

    println!("Using file {file_path}");

    let contents = fs::read_to_string(file_path)
        .expect("Should have been able to read the file");


    let (ordering, updates) = parse_input(&contents);

    // debug print
    // println!("{:?}", ordering);
    // println!("{:?}", updates);

    println!("Part one: {:?}", part_one(&ordering, &updates));
    println!("Part two: {:?}", part_two(&ordering, &updates));

}


fn parse_input(contents: &str) -> (HashMap<i32, HashSet<i32>>, Vec<Vec<i32>>) {
    let parts: Vec<&str> = contents.split("\n\n").collect();

    // Parse ordering rules into a HashMap
    let mut ordering: HashMap<i32, HashSet<i32>> = HashMap::new();

    for line in parts[0].lines() {
        if line.trim().is_empty() {
            continue;
        }
        let nums: Vec<i32> = line.split('|')
            .map(|n| n.trim().parse::<i32>().unwrap())
            .collect();

        // Add the rule: nums[0] must come before nums[1]
        ordering.entry(nums[0])
            .or_insert_with(HashSet::new)
            .insert(nums[1]);
    }

    // Parse updates into Vec<Vec<i32>>
    let updates: Vec<Vec<i32>> = parts[1]
        .lines()
        .filter(|line| !line.trim().is_empty())
        .map(|line| {
            line.split(',')
                .map(|n| n.trim().parse::<i32>().unwrap())
                .collect()
        })
        .collect();

    (ordering, updates)
}

fn part_one(ordering: &HashMap<i32, HashSet<i32>>, updates: &Vec<Vec<i32>>) -> i32 {
    let mut result = 0;

    for update in updates {
        if check_update(ordering, update) {
            result += get_middle_value(update);
        }
    }

    result
}


fn part_two(ordering: &HashMap<i32, HashSet<i32>>, updates: &Vec<Vec<i32>>) -> i32 {
    // for incorrect updates ONLY, sort them using custom ordering
    // then sum their middle values

    let mut result = 0;

    for update in updates {
        if !check_update(ordering, update) {
            let mut sorted = update.clone();
            // sort based on ordering hashmap
            sorted.sort_by(|a, b| compare_values(a, b, ordering));
            result += get_middle_value(&sorted);
        }
    }

    result
}


fn check_update(ordering: &HashMap<i32, HashSet<i32>>, update: &Vec<i32>) -> bool {
    // for each update, check if it is valid, exiting early if not

    let mut valid = true;

    for i in 0..update.len() - 1 {
        let before = update[i];
        let after = update[i + 1];

        if !ordering.contains_key(&before) || !ordering[&before].contains(&after) {
            valid = false;
            break;
        }
    }

    valid
}

fn get_middle_value(update: &Vec<i32>) -> i32 {
    // get the middle value of the update

    // assert length is odd - we're not told how to handle middle otherwise
    assert_eq!(update.len() % 2, 1);

    // return the middle value
    update[update.len() / 2]

}


fn compare_values(a: &i32, b: &i32, ordering: &HashMap<i32, HashSet<i32>>) -> Ordering {
    // If a must come before b according to ordering
    if ordering.get(a).map_or(false, |set| set.contains(b)) {
        return Ordering::Less;
    }
    // If b must come before a according to ordering
    if ordering.get(b).map_or(false, |set| set.contains(a)) {
        return Ordering::Greater;
    }
    // If no explicit ordering, maintain original order
    Ordering::Equal
}
