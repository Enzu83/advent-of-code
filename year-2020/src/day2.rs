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

#[derive(Debug)]
struct Policy {
    letter: char,
    min: u32,
    max: u32,
}

fn parse_policy_and_password(line: &str) -> (Policy, String) {
    let mut splited_line = line.split_ascii_whitespace();

    // range of the policy
    let range: Vec<u32> = splited_line.next().unwrap()
        .split('-')
        .map(|s| s.parse::<u32>().unwrap())
        .collect();

    let (min, max) = (range[0], range[1]);

    // letter used for the policy
    let letter = splited_line.next().unwrap()
        .chars().next().unwrap();

    // password to test
    let password = splited_line.next().unwrap().to_string();

    let policy = Policy {
        letter,
        min,
        max,
    };

    (policy, password)
}

fn count_occurrences_in_string(string: &String, occurrence: char) -> u32 {
    let mut count_occurrences = 0;
    
    for c in string.chars() {
        if c == occurrence {
            count_occurrences += 1;
        }
    }

    count_occurrences
}

fn puzzle_1(mut input: File) {
    let password_list: Vec<(Policy, String)> = read_input(&mut input).lines()
        .map(|line| parse_policy_and_password(line))
        .collect();

    let mut correct_passwords = 0;

    for (policy, password) in password_list {
        let occurrences = count_occurrences_in_string(&password, policy.letter);

        if policy.min <= occurrences && occurrences <= policy.max {
            correct_passwords += 1
        }
    }

    println!("Correct passwords: {}", correct_passwords);
}

fn puzzle_2(mut input: File) {
    println!("{}", read_input(&mut input));
}