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

    let instructions: Vec<i32> = input.trim()
        .split("\n")
        .map(|s| s.parse().unwrap())
        .collect();

    let mut program = Program::new(instructions.clone(), Rule::INCREASE);

    let mut steps = 0;
    while !program.has_exited() {
        program.jump_to_next_instruction();
        steps += 1;
    }

    println!("Steps required before leaving program: {}", steps);

    let mut program = Program::new(instructions.clone(), Rule::VARIABLE);

    let mut steps = 0;
    while !program.has_exited() {
        program.jump_to_next_instruction();
        steps += 1;
    }

    println!("Steps required before leaving program with variable modifications: {}", steps);

    Ok(())
}

// how instruction values are updated after a jump
enum Rule {
    INCREASE,
    VARIABLE,
}

struct Program {
    pointer: i32,
    instructions: Vec<i32>,
    rule: Rule
}

impl Program {
    pub fn new(instructions: Vec<i32>, rule: Rule) -> Self {
        Self { 
            pointer: 0,
            instructions,
            rule,
        }
    }

    pub fn jump_to_next_instruction(&mut self) {
        let offset = self.instructions[self.pointer as usize];

        self.update_instruction_value();

        self.pointer += offset; // move pointer
    }

    fn update_instruction_value(&mut self) {
        match self.rule {
            Rule::INCREASE => self.instructions[self.pointer as usize] += 1,
            Rule::VARIABLE => {
                if self.instructions[self.pointer as usize] >= 3 {
                    self.instructions[self.pointer as usize] -= 1;
                } else {
                    self.instructions[self.pointer as usize] += 1;
                }
            }
        }
    }

    pub fn has_exited(&self) -> bool {
        self.pointer < 0 || self.pointer as usize >= self.instructions.len()
    }
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn program_exit() {
        let instructions = vec![0, 3, 0, 1, -3];

        let mut program = Program::new(instructions, Rule::INCREASE);

        let mut steps = 0;
        while !program.has_exited() {
            program.jump_to_next_instruction();
            steps += 1;
        }

        assert_eq!(steps, 5);
    }

    #[test]
    fn program_exit_variable_rule() {
        let instructions = vec![0, 3, 0, 1, -3];

        let mut program = Program::new(instructions, Rule::VARIABLE);

        let mut steps = 0;
        while !program.has_exited() {
            program.jump_to_next_instruction();
            steps += 1;
        }

        assert_eq!(steps, 10);
    }
}