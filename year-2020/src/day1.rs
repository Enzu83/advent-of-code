use std::{fs::File, io::Read};

use std::cmp::Ordering;
use std::option::Option::{Some, None};

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

fn find_sum_combination(expenses: &[i32], sum: i32) -> Option<(usize, usize)> {
    let mut left_idx = 0;
    let mut right_idx = expenses.len() - 1;

    // move left or right pointers depending on their sum
    // since left value is always less than right value, we know which pointer to move for each case
    while left_idx < right_idx {
        match (expenses[left_idx] + expenses[right_idx]).cmp(&sum) {
            Ordering::Less => left_idx += 1,
            Ordering::Greater => right_idx -= 1,
            Ordering::Equal => break,
        }
    }

    if left_idx == right_idx {
        // no solution found
        None
    } else {
        // solution found
        Some((left_idx, right_idx))
    }   
}

fn puzzle_1(mut input: File) {
    let mut expenses: Vec<i32> = read_input(&mut input).lines()
        .map(|s| s.parse::<i32>().unwrap())
        .collect();

    expenses.sort();

    let (left_idx, right_idx) = find_sum_combination(&expenses, 2020).unwrap();

    println!("Found matching combination: ({}, {}). Product: {}", 
        expenses[left_idx], 
        expenses[right_idx], 
        expenses[left_idx] * expenses[right_idx]
    );
}

fn puzzle_2(mut input: File) {
    let mut expenses: Vec<i32> = read_input(&mut input).lines()
        .map(|s| s.parse::<i32>().unwrap())
        .collect();

    expenses.sort();

    // we will progressively decrease this pointer until we find a combination
    // which sum is 2020 - expenses[right_idx]
    let mut right_idx = expenses.len() - 1;

    while right_idx > 0 {
        match find_sum_combination(&expenses[0..right_idx], 2020 - expenses[right_idx]) {
            // try again with the previous expense
            None => right_idx -= 1,

            // solution found
            Some((left_idx, middle_idx)) => {
                println!("Found matching combination: ({}, {}, {}). Product: {}", 
                    expenses[left_idx], 
                    expenses[middle_idx], 
                    expenses[right_idx], 
                    expenses[left_idx] * expenses[middle_idx] * expenses[right_idx]
                );

                break
            },
        }
    }
}