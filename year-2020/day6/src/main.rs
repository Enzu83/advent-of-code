use std::{collections::HashMap, error::Error, fs::File, io::Read};

fn main() -> Result<(), Box<dyn Error>> {
    // read input
    let input = read_input("inputs/day6.txt")?;
    
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

fn get_groups(input: &String) -> Vec<String> {
    input
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

fn part_1(input: &String) {
    let groups = get_groups(input);

    let mut yes_answers: u32 = 0;

    for group in groups {
        let group: Vec<&str> = group.split_whitespace().collect();
        yes_answers += count_group_answers(&group).len() as u32;
    }

    println!("Yes answers: {}", yes_answers);
}

fn part_2(input: &String) {
    let groups = get_groups(input);

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
