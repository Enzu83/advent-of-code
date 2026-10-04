use std::{fs::File, io::Read};

fn main() -> anyhow::Result<()> {
    let mut input_file = File::open("./input.txt")?;
    let mut input = String::new();
    input_file.read_to_string(&mut input)?;

    part_1(&input);

    Ok(())
}

fn get_first_and_last_digit(line: &str) -> (u32, u32) {
    let mut first = None;
    let mut second = None;

    for char in line.chars() {
        if let Some(digit) = char.to_digit(10) {
            if first.is_none() {
                first = Some(digit);
            }

            second = Some(digit);
        }
    }

    (first.unwrap(), second.unwrap())
}

fn part_1(input: &str) {
    let mut sum = 0;

    for line in input.lines() {
        let digits = get_first_and_last_digit(line);
        sum += format!("{}{}", digits.0, digits.1).parse::<u32>().unwrap();
    }

    println!("Sum of calibration values: {}", sum);
}
