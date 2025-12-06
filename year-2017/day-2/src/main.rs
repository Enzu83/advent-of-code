use std::{env, u32};
use std::fs::File;
use std::io::Read;
use std::error::Error;

fn get_input() -> Result<String, Box<dyn Error>> {
    let input_path = match env::args().nth(1) {
        Some(path) => path,
        None => panic!("Please specify a path for the input file."),
    };
    let mut file = File::open(input_path)?;
    let mut input = String::new();
    file.read_to_string(&mut input)?;

    Ok(input)
}

fn main() -> Result<(), Box<dyn Error>> {
    let input = get_input()?;

    let spreadsheet = parse_input(&input);
    
    let checksum = compute_checksum(&spreadsheet);
    println!("Checksum: {}", checksum);

    let evenly_value_checksum = compute_evenly_value_checksum(&spreadsheet);
    println!("Evenly value checksum: {}", evenly_value_checksum);

    Ok(())
}

fn parse_input(input: &str) -> Vec<Vec<u32>> {
    let mut vec = Vec::new();

    for row in input.trim().split("\n") {
        let row_vec = row.split_whitespace().map(|s| s.parse().unwrap()).collect();
        vec.push(row_vec);
    }

    vec
}

fn get_min_max(vec: &Vec<u32>) -> (u32, u32) {
    let mut min = vec[0];
    let mut max = vec[0];

    for value in vec {
        if *value < min {
            min = *value;
        }
        if *value > max {
            max = *value;
        }
    }

    (min, max)
}

fn compute_checksum(spreadsheet: &Vec<Vec<u32>>) -> u32 {
    let mut checksum = 0;

    for list in spreadsheet {
        let (min, max) = get_min_max(list);
        checksum += max - min;
    }

    checksum
}

fn compute_evenly_value_checksum(spreadsheet: &Vec<Vec<u32>>) -> u32 {
    let mut checksum = 0;

    for list in spreadsheet {
        checksum += get_evenly_value(list);
    }

    checksum
}

fn get_evenly_value(vec: &Vec<u32>) -> u32 {
    for value in vec {
        for divisor in vec {
            if *divisor < *value && *value % *divisor == 0 {
                return *value / *divisor;
            }
        }
    }

    return 0;
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn checksum() {
        let raw_spreadsheet = "5 1 9 5
7 5 3
2 4 6 8
";
        let checksum = compute_checksum(&parse_input(raw_spreadsheet));
        assert_eq!(checksum, 18);
    }

    #[test]
    fn evenly_value_checksum() {
        let raw_spreadsheet = "5 9 2 8
9 4 7 3
3 8 6 5
";
        let checksum = compute_evenly_value_checksum(&parse_input(raw_spreadsheet));
        assert_eq!(checksum, 9);
    }
}