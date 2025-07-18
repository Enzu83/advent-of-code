use std::{fs::File, io::Read};

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
    println!("{}", read_input(&mut input));
}

fn puzzle_2(mut input: File) {
    println!("{}", read_input(&mut input));
}