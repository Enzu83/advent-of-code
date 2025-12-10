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

    let banks = input.trim()
        .split("\n")
        .map(|bank| Bank::from(bank))
        .collect::<Result<Vec<_>, Box<dyn Error>>>()?;

    let sum_of_largest_joltage: u32 = banks.iter()
        .map(|b| b.largest_voltage())
        .sum();

    println!("Sum of largest voltage: {}", sum_of_largest_joltage);

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

    pub fn largest_voltage(&self) -> u32 {
        let mut max_joltage = 0;
        let mut indexes = HashSet::new();

        // get position of maximum joltages
        for (idx, joltage) in self.batteries[..self.batteries.len()-1].iter().enumerate() {
            match joltage.cmp(&max_joltage) {
                std::cmp::Ordering::Greater => {
                    max_joltage = *joltage;
                    indexes.clear();
                    indexes.insert(idx);
                },
                std::cmp::Ordering::Equal => {
                    indexes.insert(idx);
                },
                _ => {},
            };
        }

        let mut largest_joltage = 0;

        for max_idx in indexes {
            let max_remaining_joltage = self.batteries[max_idx+1..].iter().max().unwrap();
            
            let combined_joltage: u32 = format!("{}{}", self.batteries[max_idx], max_remaining_joltage).parse().unwrap();
            if combined_joltage > largest_joltage {
                largest_joltage = combined_joltage
            }
        }

        largest_joltage
    }
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
    fn largest_voltage() {
        let bank_1 = Bank::new(vec![6, 5, 1]).unwrap();
        assert_eq!(bank_1.largest_voltage(), 65);

        let bank_2 = Bank::new(vec![7, 1, 9]).unwrap();
        assert_eq!(bank_2.largest_voltage(), 79);

        let bank_3 = Bank::new(vec![5, 5, 6]).unwrap();
        assert_eq!(bank_3.largest_voltage(), 56);
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

        let sum_of_largest_joltage: u32 = banks.iter()
            .map(|b| b.largest_voltage())
            .sum();

        assert_eq!(sum_of_largest_joltage, 357);
    }
}