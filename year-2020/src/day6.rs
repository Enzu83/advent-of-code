use std::{collections::HashMap, fs::File, io::Read};

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

fn get_groups(input: &mut File) -> Vec<String> {
    read_input(input)
        .split("\n\n")
        .map(|s| s.to_string())
        .collect::<Vec<String>>()
}

fn count_group_answers(group: &[&str]) -> HashMap<char, usize> {
    let mut group_answers = HashMap::new();

    for answers_list in group {
        for answer in answers_list.chars() {
            *group_answers.entry(answer).or_insert(0) += 1;
        }
    }

    group_answers
}

fn puzzle_1(mut input: File) {
    let groups = get_groups(&mut input);

    let mut yes_answers: u32 = 0;

    for group in groups {
        let group: Vec<&str> = group.split_whitespace().collect();
        yes_answers += count_group_answers(&group).len() as u32;
    }

    println!("Yes answers: {}", yes_answers);
}

fn puzzle_2(mut input: File) {
    let groups = get_groups(&mut input);

    let mut yes_answers = 0;

    for group in groups {
        let group: Vec<&str> = group.split_whitespace().collect();

        for (_, count) in count_group_answers(&group) {
            if count == group.len() {
                yes_answers += 1;
            }
        }
    }

    println!("Yes answers: {}", yes_answers);
}