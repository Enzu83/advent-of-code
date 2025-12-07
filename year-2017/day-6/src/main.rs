use std::collections::HashMap;
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

    let banks_state: Vec<u32> = input.split_whitespace().map(|s| s.parse().unwrap()).collect();
    let mut banks = Banks::new(banks_state);

    banks.reallocate();

    while !banks.already_seen() {
        banks.reallocate();
    }

    println!("Steps before having a loop: {}", banks.steps);
    println!("Loop length: {}", banks.steps - banks.seen[&banks.current]);

    Ok(())
}

struct Banks {
    current: Vec<u32>,
    seen: HashMap<Vec<u32>, u32>,
    steps: u32,
}

impl Banks {
    pub fn new(state: Vec<u32>) -> Self {
        let mut banks = Self { 
            current: state,
            seen: HashMap::new(),
            steps: 0,
        };
        banks.register_state();

        banks
    }

    pub fn reallocate(&mut self) {
        self.register_state();

        let mut idx = self.get_most_loaded_bank_index();
        let blocks = self.current[idx];
        
        self.current[idx] = 0;

        for _ in 0..blocks {
            idx  = (idx + 1) % self.current.len();
            self.current[idx] += 1;
        }

        self.steps += 1;
    }

    fn get_most_loaded_bank_index(&self) -> usize {
        let mut max_idx = 0;

        for (idx, block) in self.current.iter().enumerate() {
            if *block > self.current[max_idx] {
                max_idx = idx;
            }
        }

        max_idx
    }

    fn register_state(&mut self) {
        self.seen.insert(self.current.clone(), self.steps);
    }

    pub fn already_seen(&self) -> bool {
        self.seen.contains_key(&self.current)
    }
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn reallocation() {
        let mut banks = Banks::new(vec![0, 2, 7, 0]);
        banks.reallocate();

        assert_eq!(banks.current, vec![2, 4, 1, 2]);
    }

    #[test]
    fn find_loop() {
        let mut banks = Banks::new(vec![0, 2, 7, 0]);
        
        banks.reallocate();

        while !banks.already_seen() {
            banks.reallocate();
        }

        assert_eq!(banks.steps, 5);
    }

    #[test]
    fn loop_length() {
        let mut banks = Banks::new(vec![0, 2, 7, 0]);
        
        banks.reallocate();

        while !banks.already_seen() {
            banks.reallocate();
        }

        assert_eq!(banks.steps - banks.seen[&banks.current], 4);
    }
}