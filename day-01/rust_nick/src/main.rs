use std::env;
use std::fs;

fn counter(num: i64, vec: &Vec<i64>) -> i64 {
   return vec.iter().filter(|&n| *n == num).count().try_into().unwrap();
}

fn main() {
   let contents = fs::read_to_string("input.txt")
       .expect("Should be able to read file");

   let mut list1: Vec<i64> = Vec::new();
   let mut list2: Vec<i64> = Vec::new();

   for line in contents.lines() {
       let numbers: Vec<&str> = line.split("   ").collect();
       list1.push(numbers[0].parse().unwrap());
       list2.push(numbers[1].parse().unwrap());
   }
   list1.sort();
   list2.sort();

   // part 1
   let mut diff: Vec<i64> = Vec::new();
   for i in 0..list1.len() {
       diff.push((list1[i] - list2[i]).abs());
   }
   let sum: i64 = diff.iter().sum();
   println!("Part 1: {sum}");

   // part 2
   let mut total = 0;
   for i in list1 {
       total += i * counter(i, &list2);
   }
   println!("Part 2: {total}");

}
