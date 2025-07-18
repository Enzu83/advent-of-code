use std::{fs::File, io::Read};

use std::cmp::Ordering;

pub fn run_puzzle(puzzle: u8, input: File) {
    match puzzle {
        1 => puzzle_1(input),
        2 => puzzle_2(input),
        other => panic!("Unknown puzzle number: {}", other),
    }
}

fn read_input(input: &mut File) -> String {
    let mut content = String::new();
    match input.read_to_string(&mut content) {
        Ok(_) => return content,
        Err(e) => panic!("Couldn't read the input: {}", e),
    }
}

fn puzzle_1(mut input: File) {
    let mut expenses: Vec<i32> = read_input(&mut input).lines()
        .map(|s| s.parse::<i32>().unwrap())
        .collect();

    expenses.sort();

    let mut left_idx = 0;
    let mut right_idx = expenses.len() - 1;

    while left_idx < right_idx {
        match (expenses[left_idx] + expenses[right_idx]).cmp(&2020) {
            Ordering::Less => left_idx += 1,
            Ordering::Greater => right_idx -= 1,
            Ordering::Equal => break,
        }
    }
    
    println!("Found matching combination: ({}, {}). Product: {}", 
        expenses[left_idx], 
        expenses[right_idx], 
        expenses[left_idx] * expenses[right_idx]
    );

}

fn puzzle_2(mut input: File) {
    println!("{}", read_input(&mut input));
}