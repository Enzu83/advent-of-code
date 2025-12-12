use std::cmp::max;
use std::collections::VecDeque;
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

    let banks = input.trim()
        .split("\n")
        .map(|bank| Bank::from(bank))
        .collect::<Result<Vec<_>, Box<dyn Error>>>()?;

    let sum_of_largest_joltage: u64 = banks.iter()
        .map(|b| b.largest_joltage(2))
        .sum();

    println!("Sum of largest voltage (2): {}", sum_of_largest_joltage);

    let sum_of_largest_joltage_12: u64 = banks.iter()
            .map(|b| b.largest_joltage(12))
            .sum();

    println!("Sum of largest voltage (12): {}", sum_of_largest_joltage_12);

    Ok(())
}

struct Bank {
    batteries: Vec<u32>,
}

impl Bank {
    pub fn new(batteries: Vec<u32>) -> Result<Self, Box<dyn Error>> {
        match batteries.len().cmp(&2) {
            std::cmp::Ordering::Less => Err(format!("A bank need to have at least 2 batteries, invalid: {:?}", batteries).into()),
            _ => Ok(Self { batteries }),
        }
    }

    pub fn from(bank: &str) -> Result<Self, Box<dyn Error>> {
        let batteries = bank.chars()
            .map(|c| c.to_digit(10).ok_or_else(|| format!("Invalid char: {}", c).into()))
            .collect::<Result<Vec<_>, Box<dyn Error>>>()?;

        Self::new(batteries)
    }

    pub fn largest_joltage(&self, length: usize) -> u64 {
        let mut max_joltage = 0;
        let mut remaining = argmax(&self.batteries[..self.batteries.len()-length+1]);

        while !remaining.is_empty() {
            let (idx, value) = remaining.pop_front().unwrap();
            let value_length = format!("{value}").len();

            for (digit_idx, digit) in argmax(&self.batteries[idx+1..self.batteries.len()-length+1+value_length]) {
                let new_value = format!("{value}{digit}").parse().unwrap();
                
                if format!("{new_value}").len() == length {
                    max_joltage = max(max_joltage, new_value);
                } else {
                    remaining.push_back((idx+1+digit_idx, new_value));
                }
                
            }
        }

        max_joltage
    }
}

fn argmax(vec: &[u32]) -> VecDeque<(usize, u64)> {
    let max = vec.iter().max().unwrap();
    
    vec.iter()
        .enumerate()
        .filter(|(_, v)| *v == max)
        .map(|(i, v)| (i, *v as u64))
        .collect()
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn new_bank() {
        let bank = Bank::from("1234").unwrap();
        assert_eq!(vec![1, 2, 3, 4], bank.batteries);
    }

    #[test]
    fn largest_joltage() {
        let bank_1 = Bank::new(vec![6, 5, 1]).unwrap();
        assert_eq!(bank_1.largest_joltage(2), 65);

        let bank_2 = Bank::new(vec![7, 1, 9]).unwrap();
        assert_eq!(bank_2.largest_joltage(2), 79);

        let bank_3 = Bank::new(vec![5, 5, 6]).unwrap();
        assert_eq!(bank_3.largest_joltage(2), 56);
    }

    #[test]
    fn largest_joltage_12() {
        let bank = Bank::new(vec![8, 1, 8, 1, 8, 1, 9, 1, 1, 1, 1, 2, 1, 1, 1]).unwrap();
        assert_eq!(bank.largest_joltage(12), 888911112111);
    }

    #[test]
    fn example() {
        let input = "987654321111111
811111111111119
234234234234278
818181911112111";

        let banks: Vec<Bank> = input.trim()
            .split("\n")
            .map(|bank| Bank::from(bank))
            .collect::<Result<Vec<_>, Box<dyn Error>>>().unwrap();

        let sum_of_largest_joltage: u64 = banks.iter()
            .map(|b| b.largest_joltage(2))
            .sum();

        assert_eq!(sum_of_largest_joltage, 357);

        let sum_of_largest_joltage_12: u64 = banks.iter()
            .map(|b| b.largest_joltage(12))
            .sum();

        assert_eq!(sum_of_largest_joltage_12, 3121910778619);
    }
}
