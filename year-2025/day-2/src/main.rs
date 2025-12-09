use std::collections::HashSet;
use std::env;
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

    let ranges = get_ranges(&input);

    let sum_invalid: u32 = ranges
        .iter()
        .map(|r| r.invalid_ids().iter().sum::<u32>())
        .sum();

    println!("Sum of the invalid IDs: {}", sum_invalid);

    Ok(())
}

struct Range {
    min: u32,
    max: u32,
}

impl Range {
    pub fn new(min_max: &str) -> Result<Self, Box<dyn Error>> {
        let (min, max) = min_max.split_once("-").unwrap();

        Ok(Self {
            min: min.parse()?,
            max: max.parse()?,
        })
    }

    pub fn invalid_ids(&self) -> Vec<u32> {
        let mut invalid = Vec::new();

        for id in self.min..self.max+1 {
            if self.is_invalid(id) {
                invalid.push(id);
            }
        }

        invalid
    }

    fn is_invalid(&self, number: u32) -> bool {
        let string = number.to_string();

        // invalid IDs have even lengths
        if string.len() % 2 != 0 {
            return true;
        }

        let mut patterns = HashSet::new();
        for i in 0..string.len() {
            for j in i+1..string.len() {
                let pattern = &string[i..j];
                if patterns.contains(pattern) {
                    return false;
                } else {
                    patterns.insert(pattern);
                }
            }
        }

        return true;
    }
}


fn get_ranges(raw_ranges: &str) -> Vec<Range> {
    raw_ranges
        .trim()
        .split(",")
        .map(|s| Range::new(s).unwrap())
        .collect()
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn invalid_id_sum_example() {
        let input = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124";
    
        let ranges = get_ranges(input);

         let sum_invalid: u32 = ranges
        .iter()
        .map(|r| r.invalid_ids().iter().sum::<u32>())
        .sum();

        assert_eq!(sum_invalid, 1227775554);
    }
}