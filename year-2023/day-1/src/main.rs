use std::{fs::File, io::Read};

fn main() -> anyhow::Result<()> {
    let mut input_file = File::open("./input.txt")?;
    let mut input = String::new();
    input_file.read_to_string(&mut input)?;

    part_1(&input);

    Ok(())
}

fn get_digits(line: &str) -> Vec<(usize, u32)> {
    line.chars()
        .enumerate()
        .filter_map(|(i, c)| c.to_digit(10).map(|d| (i, d)))
        .collect()
}

fn get_first_and_last_digit(line: &str) -> (u32, u32) {
    let digits = get_digits(line);

    let first = digits.first()
        .map(|(_, d)| d)
        .unwrap()
        .clone();

    let second = digits.last()
        .map(|(_, d)| d)
        .unwrap()
        .clone();

    (first, second)
}

fn part_1(input: &str) {
    let sum: u32 = input.lines()
        .map(|l| get_first_and_last_digit(l))
        .map(|(d1, d2) | format!("{}{}", d1, d2).parse::<u32>().unwrap())
        .sum();

    println!("Sum of calibration values: {}", sum);
}
