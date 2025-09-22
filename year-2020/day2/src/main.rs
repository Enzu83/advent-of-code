use std::{error::Error, fs::File, io::Read};

fn main() -> Result<(), Box<dyn Error>> {
    // read input
    let input = read_input("inputs/day2.txt")?;
    
    // solve both parts
    part_1(&input);
    part_2(&input);

    Ok(())
}

fn read_input(file_path: &str) -> Result<String, Box<dyn Error>> {
    let mut input = File::open(file_path)?;
    
    let mut content = String::new();
    input.read_to_string(&mut content)?;
    Ok(content)
}

struct Policy {
    letter: char,
    first: u32,
    second: u32,
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
        first: min,
        second: max,
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

fn part_1(input: &String) {
    let password_list: Vec<(Policy, String)> = input.lines()
        .map(|line| parse_policy_and_password(line))
        .collect();

    let mut correct_passwords = 0;

    for (policy, password) in password_list {
        let occurrences = count_occurrences_in_string(&password, policy.letter);

        if policy.first <= occurrences && occurrences <= policy.second {
            correct_passwords += 1
        }
    }

    println!("Correct passwords: {}", correct_passwords);
}

fn part_2(input: &String) {
    let password_list: Vec<(Policy, String)> = input.lines()
        .map(|line| parse_policy_and_password(line))
        .collect();

    let mut correct_passwords = 0;

    for (policy, password) in password_list {
        // only one of them should be the letter
        if (password.chars().nth(policy.first as usize - 1).unwrap() == policy.letter) ^ (password.chars().nth(policy.second as usize - 1).unwrap() == policy.letter) {
            correct_passwords += 1;
        }
    }

    println!("Correct passwords: {}", correct_passwords);
}
